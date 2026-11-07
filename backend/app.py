import streamlit as st

st.title("Point Cloud Comparison Tool")

ref = st.file_uploader("Reference Cloud")
test = st.file_uploader("Test Cloud")

if st.button("Compare"):
    ...