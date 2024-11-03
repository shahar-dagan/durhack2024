from flask import Flask, request, session, redirect, jsonify, send_file, url_for, redirect
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

    if session.get("ai_image_urls_by_prompt") is None:
        session["ai_image_urls_by_prompt"] = {}

    if session["ai_image_urls_by_prompt"].get(text) is None:
        print(f"trying to make image with prompt: {text}")
        # image_url = some_text_to_image_function(text)
        # image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTkhAV70lOOVr2-gS3HXBVvR-wHv9IiTCmU8Q&s"
        
        image_url = get_dalle_image_url(text)

        session["ai_image_urls_by_prompt"][text] = image_url
    

    return redirect(session["ai_image_urls_by_prompt"][text])

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
    print("request content")
    print(request.get_data(as_text=True))

    print("trying to unpack request to json")
    story_data = request.get_json()
    print("story data")
    print(story_data)

    if not story_data:
        return jsonify({"error": "No data provided"}), 400

    try:
        chapters = process_story_data(story_data)
        session["chapters"] = chapters
        session["current_chapter"] = chapters[0]
        return jsonify({"message": "Story data processed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def main():
    return "http://127.0.0.1:5000" + url_for("make_image_from_text", text="a dog playing on a bouncy castle")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
