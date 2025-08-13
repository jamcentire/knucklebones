from constants import NUM_COLUMNS, COL_HEIGHT

NUM_COLUMNS = 3
COL_HEIGHT = 3


class PlayerBoard:
    def __init__(self, board: list[list[int]] = None) -> None:
        # We allow for a premade board, mostly for testing
        self.board = board or [[] for i in range(NUM_COLUMNS)]

    def col_score(self, i: int) -> int:
        total_score = 0
        for die_roll in range(1,7):
            roll_ct = self.board[i].count(die_roll)
            # Score contributed by a die roll is the sum of those rolls * the number of rolls
            roll_score = roll_ct * (roll_ct * die_roll)
            total_score += roll_score


        return total_score
    
    def total_score(self) -> int:
        total_score = 0
        for col in range(NUM_COLUMNS):
            total_score += self.col_score(col)

        return total_score
    
    # Modifies the col in place to add the rolled die
    def add_die_to_col(self, col_num: int, die_roll: int):
        if len(self.board[col_num]) >= COL_HEIGHT:
            raise Exception('Trying to add die to full column')

        self.board[col_num].append(die_roll)

    # Modifies the col in place to remove all instances of the die_roll number
    def remove_dice_from_col(self, col_num: int, die_roll: int):
        self.board[col_num] = [roll for roll in self.board[col_num] if roll != die_roll]


# Manages the overall board state
class GameBoard:
    def __init__(self, game_board: list[PlayerBoard] = None):
        self.game_board = game_board or [PlayerBoard(), PlayerBoard()]

    # Takes in a player number and returns the board "from their perspective"
    # NOTE This is expressed generally but only really works for 2 players currently
    def get_game_board_from_player_perspective(self, player_num: int = 0) -> list[PlayerBoard]:
        return [
            self.game_board[player_num].board,
            self.game_board[player_num - 1].board
        ]
    
    def add_die_to_col_for_player(self, player_num: int, col: int, die_roll: int):
        self.game_board[player_num].add_die_to_col(col, die_roll)
        self.game_board[player_num - 1].remove_dice_from_col(col, die_roll)

    # def get_board_state_from_player_perspective(self, player_num: int) -> list[list[int]]:
    #     return [self.game_board[0].board, self.game_board[1].board]