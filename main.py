from abc import ABC, abstractmethod
import random

##################################################################
########################## CONSTANTS #############################
##################################################################

NUM_COLUMNS = 3
NUM_PLAYERS = 2

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
    # This is definitely way too much abstraction lol
    def add_die_to_col(self, col_num: int, die_roll: int):
        self.board[col_num].append(die_roll)


class Strategy(ABC):
    @abstractmethod
    # Takes in a board state and die roll and returns the column in which to place the die
    # This is where all of the actual work happens
    # Accepts board_state as [my_board, opponent_board]
    # Will not return a col number for a full col
    # TODO: handle game end here
    def get_placement_column(self, board_state: list[PlayerBoard], die_roll: int) -> int:
        pass


class Player:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    # Accepts board_state as [my_board, opponent_board]
    def take_turn(self, board_state: list[PlayerBoard]):
        die_roll = random.randint(1,6)
        placement_col = self.strategy.get_placement_column(board_state, die_roll)
        board_state[0].add_die_to_col(placement_col, die_roll)


# NOTE: handles game board, which could be broken out into it's own class
class Match:
    def __init__(self, players: list[Player]):
        self.players = players
        # for player_num in range(0, NUM_PLAYERS):
        #     self.players[player_num].player_num = player_num

        # NOTE: We can't really do this with more than 2
        self.game_board = [PlayerBoard()] * NUM_PLAYERS

    # Takes in a player number and returns the board "from their perspective"
    def _get_board_state_for_player(self, player_num: int) -> list[PlayerBoard]:
        return [
            self.game_board[player_num],
            self.game_board[player_num - 1]
        ]
    
    def do_rounds(self, num_rounds: int):
        pass

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

