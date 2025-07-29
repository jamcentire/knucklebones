from unittest.mock import MagicMock, patch
import random
import pytest

from main import (
    Match,
    Player,
    PlayerBoard,
    GameBoard,
    NUM_COLUMNS
)

EMPTY_BOARD = [[] for i in range(NUM_COLUMNS)]


def test_player_board_scoring():
    test_board = PlayerBoard([
        [1,2,3], # 1 + 2 + 3 = 6
        [1,0,0], # 1 + 0 + 0 = 1
        [5,5,2] # 2 * (5 + 5) + 2 = 22
    ])
    expected_score = [6,1,22]

    for i in range(NUM_COLUMNS):
        assert test_board.col_score(i) == expected_score[i]
    assert test_board.total_score() == sum(expected_score)

def test_player_board_scoring_empty():
    test_board = PlayerBoard()

    assert test_board.board == EMPTY_BOARD
    assert test_board.total_score() == 0

def test_player_board_scoring_multiples():
    test_board = PlayerBoard([
        [1,1,3], # 2 * (1 + 1) + 3 = 7
        [6,6,6], # 3 * (6 + 6 + 6) = 54
        [5,5,3] # 2 * (5 + 5) + 3 = 23
    ])
    expected_score = [7,54,23]

    for i in range(NUM_COLUMNS):
        assert test_board.col_score(i) == expected_score[i]
    assert test_board.total_score() == sum(expected_score)

def test_add_die_to_col_will_error_if_col_full():
    test_board = PlayerBoard([
        [1,2],
        [],
        [1,2,3]
    ])

    with pytest.raises(Exception):
        test_board.add_die_to_col(2, 4)

def test_player_take_turn_modifies_board():
    with patch('random.randint', return_value=5):
        test_board = [PlayerBoard(), PlayerBoard()]
        mock_strategy = MagicMock()
        mock_strategy.get_placement_column.return_value = 1

        test_player = Player(mock_strategy)
        test_player.take_turn(test_board)
        assert test_board[0].board == [[],[5],[]]
        assert test_board[1].board == EMPTY_BOARD

# TODO rewrite
@pytest.mark.skip()
def test_match_can_do_round():
    with patch('random.randint', side_effect=[5,2]):
        mock_strategy = MagicMock()
        mock_strategy.get_placement_column.side_effect = [1,2]

        test_player_1 = Player(mock_strategy)
        test_player_2 = Player(mock_strategy)

        match = Match([test_player_1, test_player_2])
        match.do_round()

        assert match.game_board[0].board == [[],[5],[]]
        assert match.game_board[1].board == [[],[],[2]]

# TODO Implement
@pytest.mark.skip()
def test_matching_numbers_will_cancel_opponent():
    with patch('random.randint', side_effect=[5,5]):
        test_game_board = GameBoard([PlayerBoard(), PlayerBoard()])

        mock_strategy = MagicMock()
        mock_strategy.get_placement_column.side_effect = [1,1]

        test_player_1 = Player(mock_strategy)
        test_player_2 = Player(mock_strategy)

        test_player_1.take_turn(test_game_board.get_board_for_player(0))
        assert test_game_board.get_board_for_player() == [
            [[],[5],[]],
            EMPTY_BOARD
        ]

        test_player_2.take_turn(test_game_board.get_board_for_player(1))
        assert test_game_board.get_board_for_player() == [
            EMPTY_BOARD,
            [[],[5],[]]
        ]


def test_game_board_gets_board_for_player():
    p1_board = [
        [1,2,3],
        [4],
        [2,2,2]
    ]
    p2_board = [
        [6,6],
        [2,3,4],
        []
    ]
    test_game_board = GameBoard([PlayerBoard(p1_board), PlayerBoard(p2_board)])

    assert test_game_board.get_board_for_player(0) == [p1_board, p2_board]
    assert test_game_board.get_board_for_player(1) == [p2_board, p1_board]


# TODO test match ends when board full
# TODO test player num consistency?