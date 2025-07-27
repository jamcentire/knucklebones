from unittest.mock import MagicMock, patch
import random
import pytest

from main import (
    Player,
    PlayerBoard,
    Strategy,
    NUM_COLUMNS
)

EMPTY_BOARD = [[] for i in range(NUM_COLUMNS)]


def test_board_scoring():
    test_board = PlayerBoard([
        [1,2,3], # 1 + 2 + 3 = 6
        [1,0,0], # 1 + 0 + 0 = 1
        [5,5,2] # 2 * (5 + 5) + 2 = 22
    ])

    expected_score = [6,1,22]

    for i in range(NUM_COLUMNS):
        assert test_board.col_score(i) == expected_score[i]

    assert test_board.total_score() == sum(expected_score)

def test_empty_board_scoring():
    test_board = PlayerBoard()

    assert test_board.board == EMPTY_BOARD
    assert test_board.total_score() == 0

def test_multiples_board_scoring():
    test_board = PlayerBoard([
        [1,1,3], # 2 * (1 + 1) + 3 = 7
        [6,6,6], # 3 * (6 + 6 + 6) = 54
        [5,5,3] # 2 * (5 + 5) + 3 = 23
    ])

    expected_score = [7,54,23]

    for i in range(NUM_COLUMNS):
        assert test_board.col_score(i) == expected_score[i]

    assert test_board.total_score() == sum(expected_score)

def test_player_can_modify_board():
    with patch('random.randint', return_value=5):
        test_board = [PlayerBoard(), PlayerBoard()]
        mock_strategy = MagicMock()
        mock_strategy.get_placement_column.return_value = 1

        test_player = Player(mock_strategy)
        test_player.take_turn(test_board)
        assert test_board[0].board == [[],[5],[]]
        assert test_board[1].board == EMPTY_BOARD
