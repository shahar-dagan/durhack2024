from flask import (
    Flask,
    request,
    session,
    redirect,
    jsonify,
    send_file,
    url_for,
    redirect,
    render_template
)
from open_ai_script import get_dalle_image_url
from flask_cors import CORS
import requests
from io import BytesIO



app = Flask(__name__)

# app.config['SESSION_TYPE'] = 'filesystem'       # Use server-side session
# app.config['SESSION_COOKIE_SAMESITE'] = 'None'   # Required for cross-origin cookies
# app.config['SESSION_COOKIE_SECURE'] = True

app.secret_key = "secret"
build_page_url = "http://localhost:5173/"
game_page_url = "http://localhost:8502/"

default_story_data = [
    {
        "text": "Shahar went sailing",
        "buttons": {"speed up": 1, "enjoy the sunset": 2},
    },
    {"text": "Capsize", "buttons": {"enjoy the sunset": 2, "swim": 4}},
    {"text": "See the strange pattern in the sky", "buttons": {}},
    {"text": "Die", "buttons": {}},

]



@app.route("/new_chapter_from_choice")
def handle_choice():
    print("Session data: handle choice")
    print(dict(session))

    choice = request.args["choice"]

    current_chapter = session["story_data"][session.get("current_chapter_index")]
    new_chapter_i = current_chapter["buttons"].get(choice)

    if new_chapter_i is None:
        return "Invalid choice", 400

    session["current_chapter_index"] = new_chapter_i

    # return redirect(game_page_url)
    return ""


@app.route("/make_image_from_text", methods=["GET"])
def make_image_from_text():
    print("Session data: make image from text")
    print(dict(session))


    text = request.args.get("text")

    if session.get("ai_image_urls_by_prompt") is None:
        session["ai_image_urls_by_prompt"] = {}

    if session["ai_image_urls_by_prompt"].get(text) is None:
        print(f"trying to make image with prompt: {text}")
        # image_url = some_text_to_image_function(text)
        # image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTkhAV70lOOVr2-gS3HXBVvR-wHv9IiTCmU8Q&s"

        image_url = get_dalle_image_url(text)

        session["ai_image_urls_by_prompt"][text] = image_url

    image_url = session["ai_image_urls_by_prompt"][text]
    image_response = requests.get(image_url)

    if image_response.status_code == 200:
        # Convert image data to a BytesIO object for in-memory handling
        image_data = BytesIO(image_response.content)
        # Return the image as a file response without redirecting
        return send_file(image_data, mimetype="image/jpeg")


    # return redirect(session["ai_image_urls_by_prompt"][text])

    # return (
    #     send_file(image, mimetype="image/jpeg")
    #     if image
    #     else "No image generated"
    # ), 404


@app.route("/story_image_data", methods=["GET"])
def handle_request_story_image_data():
    print("Session data: story image data before")
    print(dict(session))

    # just for debug. delete me
    if session.get("current_chapter_index") is None:
        session["story_data"] = default_story_data
        session["current_chapter_index"] = 0

    print("Session data: story image data after")
    print(dict(session))

    current_chapter = session["story_data"][
        session.get("current_chapter_index")
    ]

    text = current_chapter["text"]
    button_choices = list(current_chapter["buttons"].keys())
    image_url = url_for("make_image_from_text", text=text)

    print("chapter")
    print(current_chapter)
    print("buttons")
    print(button_choices)


    return jsonify(
        {
            "text": text,
            "image_url": image_url,
            "button_choices": button_choices,
        }
    )


@app.route("/submit", methods=["POST"])
def submit():
    print("request content")
    print(request.get_data(as_text=True))

    print("trying to unpack request to json")
    story_data = request.get_json()
    print("story data")
    print(story_data)

    session["story_data"] = story_data
    session["current_chapter_index"] = 0
    return " "


# @app.route("/", methods=["GET"])
# def main():
#     return "http://127.0.0.1:5000" + url_for(
#         "make_image_from_text", text="a dog playing on a bouncy castle"
#     )


@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")



if __name__ == "__main__":
    cors = CORS(app, supports_credentials=True, origins=["*"])  # Replace with your React app's URL
    app.run(port=5000, debug=True)

    # react app url:
    react_app_url = "http://localhost:5173/"
