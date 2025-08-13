from abc import ABC, abstractmethod

from boards import PlayerBoard

class Player():
    # Takes in a list of heuristics
    def __init__(self, strategy: list):
        self.strategy = strategy

    # Accepts board_state as [my_board, opponent_board]
    # TODO make this a non abstract class
    def get_placement_column(self, board_state: list[PlayerBoard], die_roll: int):
        pass
