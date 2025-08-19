from constants import NUM_COLUMNS

from boards import PlayerBoard

class Player():
    # Takes in a list of heuristics to use in order
    # TODO always put random as last?
    def __init__(self, strategy: list):
        self.strategy = strategy

    # Accepts board_state as [my_board, opponent_board]
    def get_placement_column(self, board_state: list[PlayerBoard], die_roll: int):
        viable_cols = [i for i in range(NUM_COLUMNS)]
        for heur in self.strategy:
            cols = heur(board_state, viable_cols, die_roll)
            if len(cols) == 1:
                return cols[0]
            viable_cols = cols

        raise Exception(f'No placement choice given by strategy: {self.strategy}')
