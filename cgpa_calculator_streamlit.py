import streamlit as st
import pandas as pd
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="CGPA Calculator", page_icon="📊")
st.title("📊 CGPA Calculator (Multiple Semesters + PDF Export)")

# Function to input course data for a semester
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

# Custom semester input
semester_count = st.number_input("How many semesters?", min_value=1, max_value=10, step=1)
all_data = []

for i in range(semester_count):
    sem_name = st.text_input(f"Semester {i+1} Name", value=f"Semester {i+1}", key=f"sem_name_{i}")
    semester_data = input_courses(sem_name)
    all_data.append(semester_data)

# Function to calculate CGPA
def calculate_cgpa(grades, credits):
    total_credits = sum(credits)
    if total_credits == 0:
        return None, 0
    total_points = sum(g * c for g, c in zip(grades, credits))
    return total_points / total_credits, total_credits

# Button to calculate CGPA
if st.button("🧮 Calculate CGPA"):
    df_all = []
    total_weighted_points = 0
    total_units = 0

    for sem in all_data:
        cgpa, sem_units = calculate_cgpa(sem["grades"], sem["credits"])
        sem_df = pd.DataFrame({
            "Semester": sem["semester"],
            "Course": sem["courses"],
            "Grade Point": sem["grades"],
            "Unit": sem["credits"]
        })
        sem_df["Total Points"] = sem_df["Grade Point"] * sem_df["Unit"]
        df_all.append(sem_df)
        if cgpa is not None:
            st.success(f"{sem['semester']} CGPA: **{cgpa:.2f}**")
            total_weighted_points += cgpa * sem_units
            total_units += sem_units

    final_df = pd.concat(df_all, ignore_index=True)

    if total_units == 0:
        st.error("No valid credits found.")
    else:
        overall_cgpa = total_weighted_points / total_units
        st.subheader("🏆 Overall CGPA:")
        st.success(f"**{overall_cgpa:.2f}**")

    st.subheader("📋 Detailed Table")
    st.dataframe(final_df.style.format({"Grade Point": "{:.2f}", "Unit": "{:.1f}", "Total Points": "{:.2f}"}))

    # Export to PDF
    def generate_pdf(df, overall_cgpa):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "CGPA Report", ln=True, align="C")

        pdf.set_font("Arial", size=12)
        for sem in df["Semester"].unique():
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, f"\n{sem}", ln=True)
            pdf.set_font("Arial", size=11)
            subset = df[df["Semester"] == sem]
            for idx, row in subset.iterrows():
                pdf.cell(200, 10, f"{row['Course'] or 'N/A'} - GP: {row['Grade Point']}, Unit: {row['Unit']}, Points: {row['Total Points']}", ln=True)

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, f"\nOverall CGPA: {overall_cgpa:.2f}", ln=True)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(temp_file.name)
        return temp_file.name

    pdf_path = generate_pdf(final_df, overall_cgpa)

    with open(pdf_path, "rb") as f:
        st.download_button("📄 Download PDF Report", f, file_name="cgpa_report.pdf", mime="application/pdf")

    # Clean up temp file after download
    os.remove(pdf_path)
