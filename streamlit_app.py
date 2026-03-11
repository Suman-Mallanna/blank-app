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

    st.title("CRC1607 Summer School Application")

    first = st.text_input("First Name")
    last = st.text_input("Last Name")
    email = st.text_input("Email")
    university = st.text_input("University")
    degree = st.selectbox("Degree", ["Bachelor","Master","PhD"])
    field = st.text_input("Field")

    motivation = st.text_area("Motivation")

    cv = st.file_uploader("Upload CV")
    letter = st.file_uploader("Upload Motivation Letter")

    if st.button("Submit"):

        c.execute(
        "INSERT INTO applications VALUES (?,?,?,?,?,?,?)",
        (first,last,email,university,degree,field,motivation)
        )

        conn.commit()

        st.success("Application submitted!")

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
