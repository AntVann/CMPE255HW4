from flask import Flask, render_template, request, jsonify
from game_logic import create_character, battle, get_character_info

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create_character", methods=["POST"])
def create_char():
    data = request.json
    name = data.get("name")
    job = data.get("job")
    if name and job:
        create_character(name, job)
        return jsonify(get_character_info(name)), 201
    return jsonify({"error": "Invalid character data"}), 400


@app.route("/battle", methods=["POST"])
def battle_monster():
    data = request.json
    character_name = data.get("character_name")
    monster_name = data.get("monster_name")
    if character_name and monster_name:
        result = battle(character_name, monster_name)
        return jsonify(
            {"result": result, "character": get_character_info(character_name)}
        )
    return jsonify({"error": "Invalid battle data"}), 400


@app.route("/character/<name>")
def get_char_info(name):
    info = get_character_info(name)
    if info:
        return jsonify(info)
    return jsonify({"error": "Character not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
