import streamlit as st
import requests

# URL of your Flask app's endpoints
BASE_URL = "http://localhost:5000"


def start_story():
    """
    Sends a request to Flask to initiate the story.
    """
    try:
        response = requests.post(f"{BASE_URL}/story_data")
        response.raise_for_status()
        st.session_state["story_started"] = True
    except requests.RequestException as e:
        st.error(f"Error starting story: {e}")


def fetch_current_chapter():
    """
    Fetches the current chapter's data from Flask.
    """
    try:
        response = requests.get(f"{BASE_URL}/story_image_data")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching current chapter: {e}")
        return None


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


def display_chapter(chapter_data):
    """
    Parses and displays the current chapter data.
    """
    # Display chapter text
    st.write(chapter_data.get("text", "No text provided."))

    # Display chapter image if available
    image_url = chapter_data.get("image_url")
    if image_url:
        st.image(image_url)

    # Display button choices
    button_choices = chapter_data.get("button_choices", [])
    for choice in button_choices:
        if st.button(choice):
            choose_next_chapter(choice)
            st.experimental_rerun()  # Reload page to fetch the updated chapter


# Initialize session state
if "story_started" not in st.session_state:
    st.session_state["story_started"] = False

# Story start logic
if not st.session_state["story_started"]:
    st.write("Start the Story")
    if st.button("Start Story"):
        start_story()

# Display current chapter
else:
    chapter_data = fetch_current_chapter()
    if chapter_data:
        display_chapter(chapter_data)
