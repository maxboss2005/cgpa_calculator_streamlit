import streamlit as st
import pandas as pd

# ---------------------- USER DATA ----------------------
if "users" not in st.session_state:
    st.session_state.users = {"admin": "admin123"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# ---------------------- AUTHENTICATION FUNCTIONS ----------------------
def login_page():
    st.header("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

    st.markdown("Don't have an account? Go to the **Register** tab.")

def register_page():
    st.header("📝 Create Account")
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if new_username in st.session_state.users:
            st.warning("Username already exists.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif len(new_username.strip()) == 0 or len(new_password.strip()) == 0:
            st.error("Username and password cannot be empty.")
        else:
            st.session_state.users[new_username] = new_password
            st.success("Account created successfully! You can now log in.")

# ---------------------- GPA CALCULATOR PAGE ----------------------
def gpa_calculator():
    st.title("🎓 GradeTrack: GPA & Semester Analyzer")
    st.markdown(f"👋 Logged in as **{st.session_state.username}**")

    def input_courses(semester_id):
        st.subheader(f"📚 {semester_id}")
        num = st.number_input(f"Number of courses in {semester_id}", min_value=1, max_value=50, step=1, key=f"num_{semester_id}")
        courses, grades, credits = [], [], []
        for i in range(num):
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                course = st.text_input(f"{semester_id} - Course {i+1} Title", key=f"{semester_id}_course_{i}")
            with col2:
                grade = st.number_input(f"{semester_id} - G.P for {course or f'Course {i+1}'}", min_value=0.0, max_value=5.0, step=0.1, key=f"{semester_id}_grade_{i}")
            with col3:
                credit = st.number_input(f"{semester_id} - Unit for {course or f'Course {i+1}'}", min_value=0.0, max_value=5.0, step=0.1, key=f"{semester_id}_credit_{i}")
            courses.append(course)
            grades.append(grade)
            credits.append(credit)
        return {"semester": semester_id, "courses": courses, "grades": grades, "credits": credits}

    def calculate_cgpa(grades, credits):
        total_credits = sum(credits)
        if total_credits == 0:
            return None, 0
        total_points = sum(g * c for g, c in zip(grades, credits))
        return total_points / total_credits, total_credits

    level_count = st.number_input("How many levels? (e.g., 100, 200, 300)", min_value=1, max_value=6, step=1)
    levels_data = {}

    for i in range(level_count):
        level_name = st.text_input(f"Enter name for Level {i+1}", value=f"{(i+1)*100} Level", key=f"level_{i}")
        semester_count = st.number_input(f"How many semesters in {level_name}?", min_value=1, max_value=3, step=1, key=f"sem_count_{i}")
        semesters = []
        for j in range(semester_count):
            sem_name = st.text_input(f"{level_name} - Semester {j+1} Name", value=f"Semester {j+1}", key=f"{level_name}_sem_{j}")
            sem_data = input_courses(f"{level_name} - {sem_name}")
            semesters.append(sem_data)
        levels_data[level_name] = semesters

    if st.button("🧮 Calculate CGPA"):
        total_weighted_points = 0
        total_units = 0
        all_sem_dfs = []
        st.subheader("📊 Results by Level and Semester")
        level_cols = st.columns(len(levels_data))

        for col, (level_name, semesters) in zip(level_cols, levels_data.items()):
            with col:
                st.markdown(f"### 🎓 {level_name}")
                for sem in semesters:
                    cgpa, units = calculate_cgpa(sem["grades"], sem["credits"])
                    if units > 0:
                        df = pd.DataFrame({
                            "Course": sem["courses"],
                            "Grade Point": sem["grades"],
                            "Unit": sem["credits"]
                        })
                        df["Total Points"] = df["Grade Point"] * df["Unit"]
                        st.markdown(f"**{sem['semester']} CGPA: {cgpa:.2f}**")
                        st.dataframe(df.style.format({"Grade Point": "{:.2f}", "Unit": "{:.1f}", "Total Points": "{:.2f}"}))
                        total_weighted_points += cgpa * units
                        total_units += units
                        df["Semester"] = sem["semester"]
                        df["Level"] = level_name
                        all_sem_dfs.append(df)

        if total_units == 0:
            st.error("❌ No valid credit units found.")
        else:
            overall_cgpa = total_weighted_points / total_units
            st.subheader("🏆 Overall CGPA:")
            st.success(f"**{overall_cgpa:.2f}**")

            final_df = pd.concat(all_sem_dfs, ignore_index=True)
            html_export = final_df.to_html(index=False)
            html_export += f"<br><h3>Overall CGPA: {overall_cgpa:.2f}</h3>"

            st.download_button(
                label="📄 Download as HTML (Printable to PDF)",
                data=html_export,
                file_name="cgpa_report.html",
                mime="text/html"
            )
            st.info("💡 Open the downloaded HTML file in a browser and press **Ctrl+P** to save as **PDF**.")

# ---------------------- TABS FOR NAVIGATION ----------------------
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        login_page()
    with tab2:
        register_page()
else:
    tab1, tab2 = st.tabs(["CGPA Calculator", "Logout"])
    with tab1:
        gpa_calculator()
    with tab2:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.experimental_rerun()
