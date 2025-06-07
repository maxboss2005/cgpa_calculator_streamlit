import streamlit as st import pandas as pd

---------------------- USER DATA ----------------------

if "users" not in st.session_state: st.session_state.users = {"admin": "admin123"}

if "logged_in" not in st.session_state: st.session_state.logged_in = False st.session_state.username = ""

---------------------- AUTHENTICATION FUNCTIONS ----------------------

def login_page(): st.header("🔐 Login") username = st.text_input("Username") password = st.text_input("Password", type="password")

if st.button("Login"):
    if username in st.session_state.users and st.session_state.users[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success(f"Welcome, {username}!")
        st.experimental_rerun()
    else:
        st.error("Invalid credentials")

st.markdown("Don't have an account? Go to the **Register** tab.")

def register_page(): st.header("📝 Create Account") new_username = st.text_input("Choose a Username") new_password = st.text_input("Choose a Password", type="password") confirm_password = st.text_input("Confirm Password", type="password")

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

---------------------- GPA CALCULATOR PAGE ----------------------

def gpa_calculator(): st.title("🎓 GradeTrack: GPA & Semester Analyzer") st.markdown(f"👋 Logged in as {st.session_state.username}")

def input_courses(semester_id):
    st.subheader(f"📚 {semester_id}")
    num = st.number_input(f"Number of courses in {semester_id}", min_value=1, max_value=50, step=1, key=f"num_{semester_id}")
    courses, grades, credits = [], [], []
    for i in range(num):
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            course = st.text_input(f"{semester_id} - Course {i+1} Title", key

