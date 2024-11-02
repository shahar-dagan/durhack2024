from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=['POST'])
def recv_json():
    json_file = request.get_json()
    print(json_file)


if __name__ == "__main__":
    app.run(debug=True)
    



# redirect the user from node website game website
