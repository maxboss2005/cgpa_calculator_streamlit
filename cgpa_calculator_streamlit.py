# cgpa_calculator_streamlit.py

import streamlit as st

st.set_page_config(page_title="CGPA Calculator", page_icon="📊")

st.title("📊 CGPA Calculator")

# Input: Number of courses
num_subjects = st.number_input("Enter number of courses", min_value=1, max_value=100, step=1)

grades = []
credits = []
courses = []

# Input fields per course, arranged in a single line
if num_subjects:
    st.subheader("Enter Course Title, Grade Point (G.P), and Unit (Credit) on the same line")

    for i in range(1, num_subjects + 1):
        cols = st.columns([3, 2, 2])  # Wider column for title, smaller for GP and Unit
        with cols[0]:
            course_code = st.text_input(f"Course {i} Title", key=f"course_{i}")
        with cols[1]:
            grade = st.number_input("G.P", min_value=0, max_value=5, step=1, key=f"grade_{i}")
        with cols[2]:
            credit = st.number_input("Unit", min_value=0, max_value=5, step=1, key=f"credit_{i}")

        courses.append(course_code)
        grades.append(grade)
        credits.append(credit)

# Button to calculate CGPA
if st.button("Calculate CGPA"):
    try:
        total_points = sum(g * c for g, c in zip(grades, credits))
        total_credits = sum(credits)

        if total_credits == 0:
            st.error("Total credit units cannot be zero.")
        else:
            cgpa = total_points / total_credits
            st.success(f"✅ Your CGPA is: **{cgpa:.2f}**")

            with st.expander("📋 Detailed Breakdown"):
                for i in range(num_subjects):
                    st.write(f"{courses[i] or f'Course {i+1}'}: GP = {grades[i]}, Unit = {credits[i]}")
    except:
        st.error("❌ Please enter valid numbers for all fields.")
