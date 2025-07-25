import pytest
from main import PlayerBoard

def test_board_scoring():
    test_board = PlayerBoard([
        [1,2,3], # 1 + 2 + 3 = 6
        [1,0,0], # 1 + 0 + 0 = 1
        [5,5,2] # 2 * (5 + 5) + 2 = 22
    ])

    expected_score = [6,1,22]

    for i in range(3):
        assert test_board.get_row_score(i) == expected_score[i]

    assert test_board.get_total_score() == 29
