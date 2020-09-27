from typing import List

from flask import Flask, jsonify, request
from markdown2 import markdown

app = Flask(__name__)


@app.route("/")
def index():
    with open("index.html", "r") as f_obj:
        return f_obj.read()


@app.route("/about")
def about():
    """
    Function returns README.md as HTML.
    """
    with open("README.md", "r") as f_obj:
        content =  f_obj.read()
    return markdown(content)


@app.route("/api/make_move", methods=["POST"])
def make_move_api():
    """
    API function to expose making a XO move.
    Call receives json with board and returns new board with move.
    """
    data = request.get_json()
    new_board = make_move(data.get("board"), data.get("difficultyLevel"))
    return jsonify({"board": new_board})


def make_move(board: List[List], difficulty_level: str) -> List[List]:
    """
    Function receives board + difficulty_level and makes necessary call
        to external Prolog function (using pyswl).
    :param board: List of lists with either "", "X" or "O" for its cells.
        Board's length must equal it's height.
    :param difficulty_level: One out of "Easy", "Normal", "Hard"
    :return: The new board with move made.
    """
    if difficulty_level == "Easy":
        pass
    if difficulty_level == "Medium":
        pass
    # If Hard or some other input.
    else:
        pass
    board[0][0] = "O"
    return board


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
