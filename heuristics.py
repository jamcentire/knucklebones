import random

from constants import NUM_COLUMNS, COL_HEIGHT
from boards import PlayerBoard


''' Heuristics
Selects the optimal column/s in which to place a die, according to a specific strategy

Args:
    board_state (list): The state of the game board, expressed as [my_board, opponent_board], where each board is in list format
    viable_col_nums (list[int]): Column numbers that the heuristic should consider
    die_roll (int): the die roll to place

Returns:
    list[int]: a list of the best column/s in which to place the die, according to this heuristic
'''

#######################################################################
############################## HEURISTICS #############################
#######################################################################
# Place die randomly
def random_placement(board_state: list, viable_col_nums: list[int], die_roll: int) -> list[int]:
    open_col_nums = [i for i in range(0, NUM_COLUMNS) if len(board_state[0][i]) < COL_HEIGHT]
    return [random.choice(open_col_nums)]

# Try to delete as many of the opponent's dice as possible
def prioritize_multiples(board_state: list, viable_col_nums: list[int], die_roll: int) -> list[int]:
    return _get_col_nums_for_max_matches(
        board_state[0], viable_col_nums, die_roll
    )

# Try to create the maximum number of multiples in your own columns
def prioritize_deletion(board_state: list, viable_col_nums: list[int], die_roll: int) -> list[int]:
    return _get_col_nums_for_max_matches(
        board_state[1], viable_col_nums, die_roll
    )

#######################################################################
########################### HELPER FUNCTIONS ##########################
#######################################################################
def _get_col_nums_for_max_matches(board: list[list[int]], viable_col_nums: list[int], die_roll: int) -> list[int]:
    target_cols = []
    curr_match_ct = 0

    for col_num in range(NUM_COLUMNS):
        if col_num not in viable_col_nums:
            continue

        match_ct = board[col_num].count(die_roll)

        if match_ct == curr_match_ct:
            target_cols.append(col_num)

        elif match_ct > curr_match_ct:
            target_cols.clear()
            target_cols.append(col_num)
            curr_match_ct = match_ct

        # TODO handle failure case

    return target_cols
