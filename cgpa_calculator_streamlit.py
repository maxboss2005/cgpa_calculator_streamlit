# cgpa_calculator_streamlit.py

import streamlit as st

st.set_page_config(page_title="CGPA Calculator", page_icon="📊")

st.title("📊 CGPA Calculator")

# Input: Number of subjects
num_subjects = st.number_input("Enter number of courses", min_value=1, max_value=100, step=1)

grades = []
credits = []

# Dynamic subject input fields
if num_subjects:
    st.subheader("Enter Grade Points and Credit Hours")
    for i in range(1, num_subjects + 1):
        col1, col2 = st.columns(2)
        with col1:
            grade = st.number_input(f {i} Grade Point", min_value=0.0, max_value=5.0, step=0.1, key=f"grade_{i}")
        with col2:
            credit = st.number_input(f"Course {i} Unit", min_value=0.0, step=0.5, key=f"credit_{i}")
        grades.append(grade)
        credits.append(credit)

# Button to calculate CGPA
if st.button("Calculate CGPA"):
    try:
        total_points = sum(g * c for g, c in zip(grades, credits))
        total_credits = sum(credits)

        if total_credits == 0:
            st.error("Total credit hours cannot be zero.")
        else:
            cgpa = total_points / total_credits
            st.success(f"✅ Your CGPA is: **{cgpa:.2f}**")
    except:
        st.error("❌ Please enter valid numbers for all fields.")
