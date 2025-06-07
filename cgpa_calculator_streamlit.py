import streamlit as st 
import pandas as pd

--- Page setup ---

st.set_page_config(page_title="UniTrack - CGPA Portal", page_icon="📊")

--- Authentication state ---

if "authenticated" not in st.session_state: st.session_state.authenticated = False

--- In-memory user store ---

if "users" not in st.session_state: st.session_state.users = {}  # {username: password}

--- Login Page ---

def login_page(): st.subheader("🔐 Login") username = st.text_input("Username") password = st.text_input("Password", type="password") if st.button("Login"): if username in st.session_state.users and st.session_state.users[username] == password: st.session_state.authenticated = True st.success("Logged in successfully!") st.experimental_rerun() else: st.error("Invalid username or password")

--- Registration Page ---

def register_page(): st.subheader("📝 Register") username = st.text_input("Create a Username") password = st.text_input("Create a Password", type="password") if st.button("Register"): if username in st.session_state.users: st.warning("Username already exists") else: st.session_state.users[username] = password st.success("Account created! Please login.")

--- CGPA Calculator Page ---

def cgpa_calculator(): st.title("📊 CGPA Calculator")

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
    final_tables = ""
    all_sem_dfs = []

    for level_name, semesters in levels_data.items():
        st.markdown(f"## 🎓 {level_name}")
        final_tables += f"<h2>{level_name}</

