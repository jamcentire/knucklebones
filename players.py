from constants import NUM_COLUMNS

class Player():
    # Takes in a list of heuristics to use in order
    # TODO always put random as last?
    def __init__(self, strategy: list):
        self.strategy = strategy

    # Accepts board_state as [my_board, opponent_board]
    def get_placement_column(self, board_state: list[list[int]], die_roll: int):
        # Screen out full columns, pass the rest as options
        viable_cols = [i for i in range(NUM_COLUMNS) if len(board_state[0][i]) < 3]
        for heur in self.strategy:
            cols = heur(board_state, viable_cols, die_roll)
            if len(cols) == 1:
                return cols[0]
            viable_cols = cols

        raise Exception(f'No placement choice given by strategy: {self.strategy}')
