import streamlit as st
import pandas as pd

st.set_page_config(page_title="GradeTrack", page_icon="📊")
st.title("📊 CGPA Collator")

# Input for one semester
def input_courses(semester_id):
    st.subheader(f"📚 {semester_id}")
    num = st.number_input(f"Number of courses in {semester_id}", min_value=1, max_value=50, step=1, key=f"num_{semester_id}")
    courses, grades, credits = [], [], []
    for i in range(num):
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            course = st.text_input(f"{semester_id} - Course {i+1} Title", key=f"{semester_id}_course_{i}")
        with col2:
            grade = st.number_input(f"{semester_id} - G.P", min_value=0, max_value=5, step=1, key=f"{semester_id}_grade_{i}")
        with col3:
            credit = st.number_input(f"{semester_id} - Unit", min_value=0, max_value=5, step=1, key=f"{semester_id}_credit_{i}")
        courses.append(course)
        grades.append(grade)
        credits.append(credit)
    return {"semester": semester_id, "courses": courses, "grades": grades, "credits": credits}

# CGPA calculation
def calculate_cgpa(grades, credits):
    total_credits = sum(credits)
    if total_credits == 0:
        return None, 0
    total_points = sum(g * c for g, c in zip(grades, credits))
    return total_points / total_credits, total_credits

# Input for all levels and semesters
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

# Calculation and display
if st.button("🧮 Calculate CGPA"):
    total_weighted_points = 0
    total_units = 0
    final_tables = ""
    all_sem_dfs = []

    for level_name, semesters in levels_data.items():
        st.markdown(f"## 🎓 {level_name}")
        final_tables += f"<h2>{level_name}</h2>"

        for sem in semesters:
            cgpa, units = calculate_cgpa(sem["grades"], sem["credits"])
            if units > 0:
                df = pd.DataFrame({
                    "Course Title": sem["courses"],
                    "Grade Point": sem["grades"],
                    "Unit": sem["credits"],
                })
                df["Total Points"] = df["Grade Point"] * df["Unit"]
                st.markdown(f"**{sem['semester']} CGPA: {cgpa:.2f}**")
                st.dataframe(df.style.format({"Grade Point": "{:.2f}", "Unit": "{:.1f}", "Total Points": "{:.2f}"}))

                # For HTML export
                final_tables += f"<h4>{sem['semester']} (CGPA: {cgpa:.2f})</h4>"
                final_tables += df.to_html(index=False)
                final_tables += "<br>"

                total_weighted_points += cgpa * units
                total_units += units

                df["Level"] = level_name
                df["Semester"] = sem["semester"]
                all_sem_dfs.append(df)

    # Overall CGPA
    if total_units == 0:
        st.error("❌ No valid credit units found.")
    else:
        overall_cgpa = total_weighted_points / total_units
        st.subheader("🏆 Overall CGPA:")
        st.success(f"**{overall_cgpa:.2f}**")
        final_tables += f"<h3>Overall CGPA: {overall_cgpa:.2f}</h3>"

        # HTML Export Button
        st.download_button(
            label="📄 Download as HTML (Printable to PDF)",
            data=final_tables,
            file_name="cgpa_report.html",
            mime="text/html"
        )

        st.info("💡 Open the downloaded HTML file in a browser and press **Ctrl+P** (or Cmd+P) to export it as a PDF.")
