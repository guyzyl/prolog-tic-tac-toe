"""
Python function to bridge between server and the Prolog logic.
"""
from os import path
from typing import List, Optional
from itertools import islice

from pyswip_mt import PrologMT
from jinja2 import Template

STACK_LIMIT = 4000000000
OTHER_PLAYER_SYMBOL = lambda x: "x" if x == "O" else "o"

prolog = PrologMT()
currently_consulted = ""


def consult_board_size(board_size: int) -> None:
    """
    Generate the right sized prolog file and add it as
    consulted file to global prolog obj.
    """
    # Enlarge stack
    next(prolog.query(f"set_prolog_flag(stack_limit, {STACK_LIMIT})."))

    # Check if file matches current one being used
    global currently_consulted
    sized_file_name = f"{board_size}-tic-tac-toe.pl"
    if sized_file_name == currently_consulted:
        return

    # Check if file wasn't already generated
    if not path.exists(sized_file_name):
        # Load pl file as template
        with open("tic-tac-toe.pl", "r") as f_obj:
            template = Template(f_obj.read())

        # Generate and write new statements
        board_str = generate_prolog_winning_statements(board_size)
        with open(sized_file_name, "w") as f_obj:
            f_obj.write(template.render(board_statements=board_str))

    # Unload previous file and consult new one
    next(prolog.query(f'unload_file("{currently_consulted}").'))
    prolog.consult(sized_file_name)
    currently_consulted = sized_file_name


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

    consult_board_size(len(board))
    prolog_query = f"miniMax({difficulty_level}, {OTHER_PLAYER_SYMBOL(player_symbol)}, {prolog_board}, BestMove)"
    prolog_result = list(prolog.query(prolog_query, maxresult=1))[0].get("BestMove")

    # Return result
    result = prolog_to_board(prolog_result, len(board))
    return result


def check_is_winner(board: List[List], player_symbol: str) -> Optional[bool]:
    """
    Function receives board + symbol as input and makes call to
        external Prolog function to check if winning.
    :return: True if player wins, False if loses, None if no one wins.
    """
    prolog_board = board_to_prolog(board)

    # Check if player wins
    consult_board_size(len(board))
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

    # Create diagonal matches
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
