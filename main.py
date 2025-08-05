from abc import ABC, abstractmethod
import random

import pprint
import numpy as np

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
    def get_game_board_from_player_perspective(self, player_num: int = 0) -> list[PlayerBoard]:
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
        return self.strategy.get_placement_column(self.strategy, board_state, die_roll)


class Match:
    def __init__(self, players: list[Player], game_board: GameBoard = None):
        self.players = players
        # TODO game_board / board consistency
        self.game_board = game_board or GameBoard()
        self._game_over = False

    def _board_is_full(self, player_board):
        return all([len(col) == 3 for col in player_board])

    def run_match(self):
        rd = 0
        while not self._game_over:
            rd += 1
            # print(f'------------ BEGINNING ROUND {rd} -------------------')
            self.do_game_round()

        p1_score = self.game_board.game_board[0].total_score()
        p2_score = self.game_board.game_board[1].total_score()

        # p1 win
        if p1_score > p2_score:
            return [1,0]
        # p2 win
        elif p1_score < p2_score:
            return [0,1]
        # draw
        return [0,0]
        

    def do_game_round(self):
        for num in range(len(self.players)):
            self.do_player_turn(num)
            # TODO find a more efficient way than checking after every move
            if self._board_is_full(self.game_board.game_board[num].board):
                self._game_over = True

    # def do_rounds(self, num_rounds: int):
    def do_player_turn(self, player_num: int):
        die_roll = random.randint(1,6)
        player_board_state = self.game_board.get_game_board_from_player_perspective(player_num)
        col = self.players[player_num].get_placement_column_for_roll(player_board_state, die_roll)
        # print(f'Player {player_num}:    {die_roll} --> {col}')
        self.game_board.add_die_to_col_for_player(player_num, col, die_roll)
        # print('BOARD STATE: ')
        # pprint.pp(self.game_board.get_game_board_from_player_perspective(0))


##################################################################
######################### STRATEGIES ############################
##################################################################

# Randomly determines where to place die
class RandomStrat(Strategy):
    def get_placement_column(self, board_state: list[PlayerBoard], die_roll: int) -> int:
        # TODO decide on passing objects vs their boards (simplify this design as a whole)
        open_col_nums = [i for i in range(0, NUM_COLUMNS) if len(board_state[0][i]) < COL_HEIGHT]
        # TODO don't return full col
        return random.choice(open_col_nums)

##################################################################
########################### SERIES ###############################
##################################################################

p1 = Player(RandomStrat)
p2 = Player(RandomStrat)

SAMPLE_SIZE = 100

overall = [0,0]
for i in range(SAMPLE_SIZE):
    print(f'Running Match {i}...')
    match = Match([p1,p2])
    result = match.run_match()
    overall = np.add(overall, result)
    print(f'Result: {result}   |  Overall: {overall}')
print('----------------- RESULTS -----------------------')
print(overall)