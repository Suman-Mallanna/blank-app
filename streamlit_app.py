import streamlit as st
import sqlite3
import pandas as pd
import os

conn = sqlite3.connect("applications.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS applications (
first TEXT,
last TEXT,
email TEXT,
university TEXT,
degree TEXT,
field TEXT,
motivation TEXT
)
""")

menu = st.sidebar.selectbox(
    "Menu",
    ["Apply", "Admin Dashboard"]
)

# -------------------
# APPLICATION FORM
# -------------------

if menu == "Apply":

    st.set_page_config(page_title="CRC1607 Summer School Application", layout="centered")

    st.title("CRC1607 Summer School")
    st.subheader("Summer School 2026 – Application Form")

    st.write("""
    The CRC1607 Summer School provides interdisciplinary training in:
    - Ophthalmology
    - Eye Research
    - Ocular Inflammation
    - Lymphangiogenesis
    - Bioinformatics
    - Metabolism
         

    Please complete the application form and upload your CV and Motivation Letter.
    """)

    st.header("Personal Information")

    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    nationality = st.text_input("Nationality")

    st.header("Academic Background")

    degree = st.selectbox(
        "Current Degree",
        ["Bachelor", "Master", "PhD", "MD", "Other"]
    )

    field = st.text_input("Field of Study")
    university = st.text_input("University / Institution")
    country_uni = st.text_input("Country of University")

    year = st.selectbox(
        "Year of Study",
        ["1", "2", "3", "4", "Final Year", "Other"]
    )

    st.header("Research Experience")

    experience = st.radio("Do you have research experience?", ["Yes", "No"])

    research_desc = st.text_area("Briefly describe your research experience")


    st.header("Motivation")

    motivation = st.text_area("Why do you want to attend the CRC1607 Summer School?")

    gain = st.text_area("What do you hope to gain from this program?")

    st.header("Upload Documents")

    cv = st.file_uploader("Upload CV (PDF)", type=["pdf"])
    motivation_letter = st.file_uploader("Upload Motivation Letter (PDF)", type=["pdf"])

    st.header("Additional Information")

    travel_support = st.radio("Do you require travel support?", ["Yes", "No"])


    if st.button("Submit Application"):

        c.execute(
        "INSERT INTO applications VALUES (?,?,?,?,?,?,?)",
        (first,last,email,university,degree,field,motivation)
        )

        conn.commit()

        st.success("Application submitted!")
    else:
        st.error("Please complete filling all the details.")

# -------------------
# ADMIN DASHBOARD
# -------------------

if menu == "Admin Dashboard":

    password = st.text_input("Admin Password", type="password")

    if password == "crc1607":

        st.title("Applications")

        df = pd.read_sql("SELECT * FROM applications", conn)

        st.dataframe(df)

        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            "applications.csv"
        )

    else:
        st.warning("Admin access only")
