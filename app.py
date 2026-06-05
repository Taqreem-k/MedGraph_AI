import streamlit as st

st.title("MedGraph AI")

st.subheader("An AI EMR System for medical data in a graphical way")

st.subheader("Input the medical file:")


upload_file = st.file_uploader("Upload", type=["pdf"])

if upload_file is not None:
    st.success("File successfully uploaded!")