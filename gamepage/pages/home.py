import streamlit as st
import testy as t

des = "In Streamlit, when creating a multi-page app, each page is loaded as an independent module, and Streamlit typically adds all pages to a sidebar. If you want to navigate between pages without showing the first page or sidebar links to previous pages, you can create custom navigation logic"

if st.button("yes.py"):
    t.show_page("first page", "images/Chur Bum.jpg", des, ["yes","no"])