
import random
#import pprint
#import numpy as np

from boards import GameBoard
from players import Player

##################################################################
######################## GAME OBJECTS ############################
##################################################################

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
        col = self.players[player_num].get_placement_column(player_board_state, die_roll)
        print(f'Player {player_num}:    {die_roll} --> {col}')
        self.game_board.add_die_to_col_for_player(player_num, col, die_roll)
        # print('BOARD STATE: ')
        # pprint.pp(self.game_board.get_game_board_from_player_perspective(0))


##################################################################
######################### STRATEGIES ############################
##################################################################


##################################################################
########################### SERIES ###############################
##################################################################

'''
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
'''