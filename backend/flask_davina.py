import flask

app = flask.Flask(__name__)

build_page_url = ""
game_page_url = ""

class Chapter:
    def __init__(self, story_text):
        self.story_text = story_text
        self.buttons = []
        
    def add_button(self, description: str, chapter):
        self.buttons.append(description, chapter)


def process_story_data(story_data):
    chapters = [Chapter(chapter_dict["text"]) for chapter_dict in story_data]
    for chapter, chapter_dict in zip(chapters, story_data):
        for button_name, chapter_index in chapter_dict["buttons"].values():
            chapter.add_button(button_name, chapters[chapter_index])

    return chapters
        



@app.route("/story_data", methods=['POST'])
def handle_receive_story_data():
    json_file = flask.request.get_json()
    # extract chapters data
    chapters: list[Chapter] = process_story_data(json_file)
    # save in session
    flask.session["chapters"] = chapters
    flask.session["current_chapter"] = chapters[0]
    # redirect
    flask.redirect(game_page_url)

def some_text_to_image_function(text):
    return None


@app.route("/new_chapter_from_choice")
def handle_choice():
    choice = flask.request.args.choice
    new_chapter = flask.session["current_chapter"].buttons.get(choice)

    if new_chapter is None:
        return "invalid choice"
    
    flask.session["current_chapter"] = new_chapter

    flask.redirect(game_page_url)

@app.route("/make_image_from_text", methods=["GET"])
def make_image_from_text():
    text = flask.request.args.text
    image = some_text_to_image_function(text)

    return flask.send_file(image, mimetype='image/jpeg')




@app.route("/story_image_data", methods=["GET"])
def handle_request_story_image_data():
    text = flask.session["current_chapter"].text
    image = some_text_to_image_function(text)
    button_choices = flask.session["current_chapter"].buttons.keys()

    return flask.jsonify({
        "text": text,
        "image_url": flask.urlfor("make_image_from_text", text=text),
        "button_choices": button_choices
    })



if __name__ == "__main__":
    app.run(debug=True)
    



# redirect the user from node website game website
