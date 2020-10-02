from typing import List, Optional
from itertools import islice


from pyswip_mt import PrologMT
from flask import Flask, jsonify, request
from markdown2 import markdown

OTHER_PLAYER_SYMBOL = lambda x: "x" if x == "O" else "o"

app = Flask(__name__)

prolog = PrologMT()
prolog.consult("tic-tac-toe.pl")


@app.route("/")
def index():
    """
    Index page of server, returns index.html.
    """
    with open("index.html", "r") as f_obj:
        return f_obj.read()


@app.route("/about")
def about():
    """
    Function returns README.md as HTML.
    This is used for the "About" button in the index page.
    """
    with open("README.md", "r") as f_obj:
        content =  f_obj.read()
    return markdown(content)


@app.route("/api/is_winner", methods=["POST"])
def is_winner():
    """
    API function to expose checking for a winner in XO board.
    Call receives JSON with board + player's symbol and returns result.
    """
    data = request.get_json()
    winner_result = is_winner(data.get("board"), data.get("symbol"))
    return jsonify({"result": winner_result})


@app.route("/api/make_move", methods=["POST"])
def make_move_api():
    """
    API function to expose making a XO move.
    Call receives json with board and returns new board with move.
    """
    data = request.get_json()
    new_board = make_move(data.get("board"), data.get("difficultyLevel"), data.get("symbol"))
    return jsonify({"board": new_board})


def make_move(board: List[List], difficulty_level: int, player_symbol: str) -> List[List]:
    """
    Function receives board + difficulty_level and makes necessary call
        to external Prolog function (using pyswl).
    :param board: List of lists with either "", "X" or "O" for its cells.
        Board's length must equal it's height.
    :param difficulty_level: A number signifying the alpha-beta depth
    :param player_symbol: The symbol the computer needs to play
    :return: The new board with move made.
    """
    # Make data simpler for Prolog
    prolog_board = board_to_prolog(board)

    prolog_query = f"miniMax({difficulty_level}, {OTHER_PLAYER_SYMBOL(player_symbol)}, {prolog_board}, BestMove)"
    prolog_result = list(prolog.query(prolog_query, maxresult=1))[0].get("BestMove")

    # Return result
    result = prolog_to_board(prolog_result, len(board))
    return result


def is_winner(board: List[List], player_symbol: str) -> Optional[bool]:
    """
    Function receives board + symbol as input and makes call to
        external Prolog function to check if winning.
    :return: True if player wins, False if loses, None if no one wins.
    """
    prolog_board = board_to_prolog(board)

    # Check if player wins
    prolog_query = f"isWinning({player_symbol.lower()}, {prolog_board})."
    prolog_result = list(prolog.query(prolog_query))
    if len(prolog_result) > 0:
        return True

    # Check if computer wins
    prolog_query = f"isWinning({OTHER_PLAYER_SYMBOL(player_symbol)}, {prolog_board})."
    prolog_result = list(prolog.query(prolog_query))
    if len(prolog_result) > 0:
        return False

    return None


def board_to_prolog(board: List[List]) -> str:
    """
    Convert the board from Python object to something Prolog can digest.
    """
    board_str_list = []
    for row in board:
        for cell in row:
            board_str_list.append(cell.lower() if cell else "0")

    result = str(board_str_list).replace("'", "")
    return result

def prolog_to_board(board: List, board_size: int) -> List[List]:
    """
    Convert the board from prolog string to Python object.
    """
    board_str_list = []
    for cell in board:
        board_str_list.append("" if cell == 0 else cell.chars.decode().upper())

    iterator = iter(board_str_list)
    result = [list(islice(iterator, board_size)) for _ in range(board_size)]
    return result


def generate_prolog_winning_statements(board_size: int):
    """
    Generate the isWinning prolog statement dependent on board size.
    This is needed since it's difficult to support dynamic array
        size + matching winning statements in Prolog.
    See tic-tac-toe.pl for Prolog function documentaion.
    """
    board_array = [f"X{i}" for i in range(1, board_size * board_size + 1)]
    statements_lists = []

    # Create vertical winning matches
    for i in range(1, board_size + 1):
        statements_lists.append([f"X{i + (board_size * j)}" for j in range(board_size)])

    # Create horizontal winning matches
    for i in range(board_size):
        statements_lists.append([f"X{(i * board_size) + j}" for j in range(1, board_size + 1)])

    # If board_size is odd create diagonal matches
    if (board_size % 2 == 1):
        statements_lists.append([f"X{(i * board_size) + i + 1}" for i in range(board_size)])
        statements_lists.append([f"X{(i * board_size) + (board_size - i)}" for i in range(board_size)])

    statements_string = []
    # Add required strings
    statements_string.append(f"equal({', '.join(['X' for i in range(board_size + 1)])}).")
    statements_string.append(f"isWinning(P, [{', '.join(board_array)}]) :-")
    # Convert all statements (except last) to strings
    for statement in statements_lists[:-1]:
        statements_string.append(f"\tequal(P, {', '.join(statement)});")
    # Add last statement with "."
    statements_string.append(f"\tequal(P, {', '.join(statements_lists[-1])}).")

    full_prolog_code = "\n" + "\n".join(statements_string) + "\n"
    return full_prolog_code


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
