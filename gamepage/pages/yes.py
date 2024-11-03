import streamlit as st


st.header("MATTYYYY")
st.write("LEGENDARY")



col1, col2 = st.columns(2)
with col1:
    # centre the options
    colu1, colu2, colu3 = st.columns(3)
    with colu1:
        st.write("")
    with colu2:
        button1 = st.button("whadoimrnwnoebrnoirbnirnirivniovwniewvniwvdnoievfevnoivfoi")
    with colu3:
        st.write("")

with col2:
    colu1, colu2, colu3 = st.columns(3)
    with colu1:
        st.write("")
    with colu2:
        button2 = st.button("option B")
    with colu3:
        st.write("")