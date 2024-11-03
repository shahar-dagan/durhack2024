from flask import Flask, request, session, redirect, jsonify, send_file, url_for
from open_ai_script import get_dalle_image_url


app = Flask(__name__)
app.secret_key = "secret"
build_page_url = "http://localhost:5173/"
game_page_url = "http://localhost:8502/"


class Chapter:
    def __init__(self, story_text):
        self.story_text = story_text
        self.buttons = []

    def add_button(self, description: str, chapter):
        self.buttons.append((description, chapter))


def process_story_data(story_data):
    chapters = [Chapter(chapter_dict["text"]) for chapter_dict in story_data]
    for chapter, chapter_dict in zip(chapters, story_data):
        for button_name, chapter_index in chapter_dict["buttons"].items():
            chapter.add_button(button_name, chapters[chapter_index])

    return chapters


# @app.route("/story_data", methods=["POST"])
# def handle_receive_story_data():
#     json_file = request.get_json()
#     chapters = process_story_data(json_file)
#     session["chapters"] = chapters
#     session["current_chapter"] = chapters[0]
#     return redirect(game_page_url)


def some_text_to_image_function(text):
    # Implement this function to generate an image from text
    return None


@app.route("/new_chapter_from_choice")
def handle_choice():
    choice = request.args.get("choice")
    current_chapter = session.get("current_chapter")
    new_chapter = (
        current_chapter.buttons.get(choice) if current_chapter else None
    )

    if new_chapter is None:
        return "Invalid choice", 400

    session["current_chapter"] = new_chapter
    return redirect(game_page_url)


@app.route("/make_image_from_text", methods=["GET"])
def make_image_from_text():
    text = request.args.get("text")
    image_url = some_text_to_image_function(text)
    return image_url
    # return (
    #     send_file(image, mimetype="image/jpeg")
    #     if image
    #     else "No image generated"
    # ), 404


@app.route("/story_image_data", methods=["GET"])
def handle_request_story_image_data():
    current_chapter = session.get("current_chapter")
    if not current_chapter:
        return jsonify({"error": "No current chapter"}), 404

    text = current_chapter.story_text
    button_choices = [button[0] for button in current_chapter.buttons]
    image_url = url_for("make_image_from_text", text=text)

    return jsonify(
        {
            "text": text,
            "image_url": image_url,
            "button_choices": button_choices,
        }
    )


@app.route("/submit", methods=["POST"])
def submit():
    story_data = request.get_json()
    if not story_data:
        return jsonify({"error": "No data provided"}), 400

    try:
        chapters = process_story_data(story_data)
        session["chapters"] = chapters
        session["current_chapter"] = chapters[0]
        return jsonify({"message": "Story data processed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
