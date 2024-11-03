import streamlit as st
pages = []
page = 0
st.set_page_config(page_title="Skeleton Layout Example", layout="wide")

# Header section
st.title("TITLE")
st.image("images/Chur Bum.jpg")
st.write("lalalalalalalala okkokokokokok")


if st.button("NEXT PAGE"):
    page =+ 1