from abc import ABC, abstractmethod
import random

##################################################################
########################## CONSTANTS #############################
##################################################################

NUM_COLUMNS = 3
NUM_PLAYERS = 2
COL_HEIGHT = 3

##################################################################
######################## GAME OBJECTS ############################
##################################################################

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
    def get_board_for_player(self, player_num: int = 0) -> list[PlayerBoard]:
        return [
            self.game_board[player_num].board,
            self.game_board[player_num - 1].board
        ]
    
    def add_die_to_col_for_player(self, player_num: int, col: int, die_roll: int):
        self.game_board[player_num].add_die_to_col(col, die_roll)
        self.game_board[player_num - 1].remove_dice_from_col(col, die_roll)


class Strategy(ABC):
    @abstractmethod
    # Takes in a board state and die roll and returns the column in which to place the die
    # This is where all of the actual work happens
    # Accepts board_state as [my_board, opponent_board]
    # Will not return a col number for a full col
    # TODO: handle game end here
    def get_placement_column(self, board_state: list[PlayerBoard], die_roll: int) -> int:
        pass


# NOTE: This is currently just a pass-through for Strategy. May change later (or remove)
class Player:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    # Accepts board_state as [my_board, opponent_board]
    # TODO change name from Strategy method (or erase Player entirely)
    def get_placement_column_for_roll(self, board_state: list[PlayerBoard], die_roll: int):
        return self.strategy.get_placement_column(board_state, die_roll)


class Match:
    def __init__(self, players: list[Player]):
        self.players = players
        # TODO game_board / board consistency
        self.game_board = GameBoard()
    
    # def do_rounds(self, num_rounds: int):
    def do_player_turn(self, player_num: int):
        die_roll = random.randint(1,6)
        player_board_state = self.game_board.get_board_for_player(player_num)
        col = self.players[player_num].get_placement_column_for_roll(player_board_state, die_roll)
        self.game_board.add_die_to_col_for_player(player_num, col, die_roll)


##################################################################
######################### STRATEGIES ############################
##################################################################

# Randomly determines where to place die
class RandomStrat(Strategy):
    def get_placement_column(self, board_state: list[PlayerBoard], die_roll: int) -> int:
        open_col_nums = [i for i in range(0, NUM_COLUMNS) if len(board_state[i]) < 2]
        # TODO don't return full col
        return random.choice(open_col_nums)

##################################################################
########################### MATCHES ##############################
##################################################################

