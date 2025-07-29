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

def test_add_die_to_col():
    test_board = PlayerBoard([
        [1,2],
        [],
        [1,2,3]
    ])

    test_board.add_die_to_col(1, 4)

    assert test_board.board == [
        [1,2],
        [4],
        [1,2,3]
    ]

def test_add_die_to_col_will_error_if_col_full():
    test_board = PlayerBoard([
        [1,2],
        [],
        [1,2,3]
    ])

    with pytest.raises(Exception):
        test_board.add_die_to_col(2, 4)

def test_remove_die_from_col():
    test_board = PlayerBoard([
        [1,2],
        [],
        [1,2,3]
    ])
    test_board.remove_dice_from_col(0, 1)
    test_board.board == [
        [2],
        [],
        [1,2,3]
    ]


def test_game_board_defaults_to_empty():
    test_game_board = GameBoard()
    assert test_game_board.get_board_for_player(0) == [EMPTY_BOARD, EMPTY_BOARD]

def test_do_player_turn_modifies_board():
    with patch('random.randint', return_value=2):
        mock_player_1 = MagicMock()
        mock_player_2 = MagicMock()
        mock_player_1.get_placement_column_for_roll.return_value = 1
        test_match = Match([mock_player_1, mock_player_2])

        test_match.do_player_turn(0)

        assert test_match.game_board.get_board_for_player(0) == [
            [[],[2],[]],
            EMPTY_BOARD
        ]

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
def test_matching_opponent_die_will_erase_it():
    p1_board = PlayerBoard([
        [1,2,3],
        [4],
        []
    ])
    p2_board = PlayerBoard([
        [6,6],
        [],
        [3,1,3]
    ])
    test_game_board = GameBoard([p1_board, p2_board])
    test_game_board.add_die_to_col_for_player(0, 2, 3)

    assert test_game_board.get_board_for_player(0) == [
        [
            [1,2,3],
            [4],
            [3]
        ],
        [
            [6,6],
            [],
            [1]
        ]
    ]

def test_game_board_gets_board_for_player_perspective():
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