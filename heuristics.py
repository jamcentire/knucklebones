import random

from constants import NUM_COLUMNS, COL_HEIGHT
from boards import PlayerBoard


# All heuristics take in a board state and die roll and return the column in which they place the die
# Accepts board_state as [my_board, opponent_board]
# Will not return a col number for a full col
# Returns a col_num int for chosen column, or -1 if no col_num chosen

def random_placement(board_state: list[PlayerBoard], die_roll: int) -> int:
    open_col_nums = [i for i in range(0, NUM_COLUMNS) if len(board_state[0][i]) < COL_HEIGHT]
    return random.choice(open_col_nums)

def prioritize_multiples(board_state: list[PlayerBoard], die_roll: int) -> int:
    # open_columns = [col for col in board_state[0].board if len(col) < 2]
    target_col = -1
    curr_match_ct = 0

    for i, col in enumerate(board_state[0].board):
        match_ct = col.count(die_roll)
        if len(col) >= COL_HEIGHT or match_ct == 0:
            continue

        if match_ct > curr_match_ct:
            curr_match_ct = match_ct
            target_col = i

    return target_col