import streamlit as st

all_pages = {
    1 : ["image link","description",["options"]],
    2 : ["image link","description",["options"]]
}


def show_page(title,image, description, options): 
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "testy.py"

    # Header section
    with st.container():
        st.title(title)
        st.image(image)
        st.write(description)

    # create 2 columns for 2 options
    with st.container():
        st.columns(len(options))
        i=0
        for x in options:
            #colu1, colu2, colu3 = st.columns(3)
            #with colu1:
            #    st.write("")
            #with colu2:
            st.button(str(i+1))
            #with colu3:
            #    st.write("")
            i += 1

    #if button1:
        #show_page()
    #elif button2:
        #st.switch_page("yes.py")


def load_page(page):
    with open(page, "r") as f:
        code = f.read()
    exec(code, globals())
