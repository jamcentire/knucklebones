from unittest.mock import MagicMock, patch
#import random
import pytest

from boards import PlayerBoard, GameBoard
from players import Player
from constants import NUM_COLUMNS
from matches import Match

EMPTY_BOARD = [[] for i in range(NUM_COLUMNS)]
VIABLE_COLS = [i for i in range(NUM_COLUMNS)]

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

def test_remove_dice_from_col():
    test_board = PlayerBoard([
        [1,2],
        [],
        [2,2,3]
    ])
    test_board.remove_dice_from_col(0, 1)
    test_board.board == [
        [2],
        [],
        [2,2,3]
    ]

    test_board.remove_dice_from_col(2, 2)
    test_board.board == [
        [2],
        [],
        [3]
    ]


def test_game_board_defaults_to_empty():
    test_game_board = GameBoard()
    assert test_game_board.get_game_board_from_player_perspective(0) == [EMPTY_BOARD, EMPTY_BOARD]

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

    assert test_game_board.get_game_board_from_player_perspective(0) == [p1_board, p2_board]
    assert test_game_board.get_game_board_from_player_perspective(1) == [p2_board, p1_board]

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

    assert test_game_board.get_game_board_from_player_perspective(0) == [
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

@patch('random.randint')
def test_do_player_turn_modifies_board(mock_randint):
    mock_randint.return_value = 2
    mock_player_1 = MagicMock()
    mock_player_2 = MagicMock()
    mock_player_1.get_placement_column.return_value = 1
    test_match = Match([mock_player_1, mock_player_2])

    test_match.do_player_turn(0)

    assert test_match.game_board.get_game_board_from_player_perspective(0) == [
        [[],[2],[]],
        EMPTY_BOARD
    ]

@patch('random.randint')
@patch('random.choice')
def test_match_can_do_round(mock_choice, mock_randint):
    mock_randint.side_effect = [5,2]
    mock_choice.return_value = [0,1]
    mock_player_1 = MagicMock()
    mock_player_2 = MagicMock()
    mock_player_1.get_placement_column.return_value = 1
    mock_player_2.get_placement_column.return_value = 2

    match = Match([mock_player_1, mock_player_2])
    match._do_game_round()

    assert match.game_board.game_board[0].board == [[],[5],[]]
    assert match.game_board.game_board[1].board == [[],[],[2]]

def test_match_ends_with_winner_when_board_full():
    mock_player_1 = MagicMock()
    mock_player_2 = MagicMock()
    mock_player_1_board = MagicMock()
    mock_player_2_board = MagicMock()

    mock_player_1_board.board = []

    test_game_board = GameBoard([mock_player_1_board, mock_player_2_board])
    test_match = Match([mock_player_1, mock_player_2], test_game_board)

    mock_player_1_board.total_score.return_value = 30
    mock_player_2_board.total_score.return_value = 50

    with patch.object(Match, '_board_is_full', return_value=True):
        assert [0,1] == test_match.run_match()

def test_player_will_use_multiple_heuristics():
    test_die_roll = 1
    test_board = [EMPTY_BOARD, EMPTY_BOARD]
    test_heuristics = [MagicMock()] * 3
    test_player = Player(test_heuristics)

    test_heuristics[0].return_value = [1,2]
    test_heuristics[1].return_value = [2]

    assert test_player.get_placement_column(test_board, test_die_roll) == 2

    test_heuristics[1].assert_called_once_with(test_board, VIABLE_COLS, test_die_roll)

def test_player_will_fail_if_no_heuristics_work():
    test_heuristics = [MagicMock()] * 3
    test_player = Player(test_heuristics)

    test_heuristics[0].return_value = [0,1,2]
    test_heuristics[1].return_value = [0,1,2]
    test_heuristics[2].return_value = [0,1,2]

    with pytest.raises(Exception):
        test_player.get_placement_column([PlayerBoard(), PlayerBoard()], 1)

def test_get_placement_column_will_screen_out_full_columns():
    # col 0 is full, so we should see our heuristic called with [1,2]
    test_board = [[[1,2,1], [1], []], EMPTY_BOARD]
    test_heuristics = [MagicMock()] * 3
    test_player = Player(test_heuristics)

    test_heuristics[0].return_value = [0]
    test_player.get_placement_column(test_board, 1)
    test_heuristics[0].assert_called_once_with(test_board, [1,2], 1)
