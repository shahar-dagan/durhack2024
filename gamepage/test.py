import streamlit as st
import requests

# URL of your Flask app's endpoints
BASE_URL = "http://127.0.0.1:5000"  # Update if using ngrok or a different host


def start_story(story_data):
    """
    Sends story data to Flask to initiate the story.
    """
    try:
        response = requests.post(f"{BASE_URL}/story_data", json=story_data)
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


# Initialize session state
if "story_started" not in st.session_state:
    st.session_state["story_started"] = False

# Story start logic
if not st.session_state["story_started"]:
    st.write("Start the Story")
    # Assuming story_data is predefined or fetched separately
    story_data = [
        {"text": "Welcome to the adventure!", "buttons": {"Begin": 1}},
        {"text": "This is Chapter 1.", "buttons": {"Continue": 2, "Exit": 0}},
        # Add more chapters here...
    ]
    if st.button("Start Story"):
        start_story(story_data)

# Display current chapter
else:
    chapter_data = fetch_current_chapter()
    if chapter_data:
        # Display text and image
        st.write(chapter_data["text"])
        st.image(chapter_data["image_url"])

        # Display button choices
        for choice in chapter_data["button_choices"]:
            if st.button(choice):
                choose_next_chapter(choice)
                st.experimental_rerun()  # Reload page to fetch the updated chapter
