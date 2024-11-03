import streamlit as st
import requests

# URL of your Flask app's endpoints
BASE_URL = "http://localhost:5000"


# http get from flask
# retrieve story related from json
# return data to be displayed
def fetch_current_chapter():
    """
    Fetches the current chapter's data from Flask.
    """
    try:
        response = requests.get(f"{BASE_URL}/story_image_data")
        response.raise_for_status()
        json = response.json()
        return json
    except requests.RequestException as e:
        st.error(f"Error fetching current chapter: {e}")



# takes in a choice from buttons clicked
# make get request to server to decide new chapter

# try using redirect to go to the same page (for new chapter data)
# failing that try to refresh page
def choose_next_chapter(choice):
    """
    Sends the selected choice to Flask to navigate to the next chapter.
    """
    try:
        response = requests.get(
            f"{BASE_URL}/new_chapter_from_choice", params={"choice": choice}
        )
        response.raise_for_status()
    except requests.RequestException as e:
        st.error(f"Error making choice: {e}")


# display data about the story
# 1 text field, many buttons, 1 image
def display_chapter(chapter_data):
    """
    Parses and displays the current chapter data.
    """
    # Display chapter text
    st.write(chapter_data.get("text", "No text provided."))

    # Display chapter image if available
    image_url = chapter_data.get("image_url")
    if image_url:
        st.image(BASE_URL + image_url)

    # # Display button choices
    button_choices = chapter_data.get("button_choices", [])
    for choice in button_choices:
        if st.button(choice):
            choose_next_chapter(choice)
            # st.experimental_rerun()  # Reload page to fetch the updated chapter


# # Initialize session state
# if "story_started" not in st.session_state:
#     st.session_state["story_started"] = False

# # Story start logic
# if not st.session_state["story_started"]:
#     st.write("Start the Story")
#     if st.button("Start Story"):
#         fetch_current_chapter()


chapter_data = fetch_current_chapter()
display_chapter(chapter_data)

