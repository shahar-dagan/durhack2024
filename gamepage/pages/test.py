import streamlit as st
pages = []
page = 0
st.set_page_config(page_title="Skeleton Layout Example", layout="wide")

# Header section
st.title("TITLE")
st.subheader("lalalalalalalala okkokokokokok")

st.image("images/Chur Bum.jpg")
if st.button("NEXT PAGE"):
    page =+ 1