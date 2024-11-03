import streamlit as st

##  might be a helpful format for saving the pages but sugject to change, whatever people think is best idm
all_pages = {
    1 : ["image link","description",["options"]],
    2 : ["image link","description",["options"]]
}

# I have assumed the important information needed for the page, options is assumed as an array but can be changed
def show_page(title,image, description, options): 
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "testy.py"

    # contains all the data from the AI model
    with st.container():
        st.title(title)
        st.image(image)
        st.write(description)

    # create number of columns for number of options
    with st.container():
        st.columns(len(options))
        i=0
        for x in options:
            st.button("option" + str(i+1))
            i += 1

## for when the buttons have functionality to go to another page. calls the function again with the next pages attributes potentially
    #if button1:
        #show_page()
    #elif button2:
        #st.switch_page("yes.py")


### code that might be helpful reading a file
def load_page(page):
    with open(page, "r") as f:
        code = f.read()
    exec(code, globals())
