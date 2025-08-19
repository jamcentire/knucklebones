from heuristics import prioritize_multiples, prioritize_deletion
# TODO change naming conventions
from constants import NUM_COLUMNS

ALL_VIABLE_COLS = [i for i in range(NUM_COLUMNS)]
EMPTY_BOARD = [[] for i in range(NUM_COLUMNS)]

def test_prioritize_multiples_heuristic():
    # Should return viable_cols input if no match found
    assert [0,2] == prioritize_multiples([
        [[1,2],[4],[]],
        EMPTY_BOARD,
    ], [0,2], 5)

    # Should return column with matching number if exists
    assert [1] == prioritize_multiples([
        [[1,2],[4],[]],
        EMPTY_BOARD
    ], ALL_VIABLE_COLS, 4)

    # Should prioritize greater number of multiples if several columns contain matches
    assert [2] == prioritize_multiples([
        [[2],[],[2,2]],
        EMPTY_BOARD
    ], ALL_VIABLE_COLS, 2)

    # Should return all columns with max matches, if multiple exist
    assert [0,2] == prioritize_multiples([
        [[2],[1],[2]],
        EMPTY_BOARD
    ], ALL_VIABLE_COLS, 2)


def test_prioritize_deletion_heuristic():
    # Should return viable_cols input if no match found
    assert [0,2] == prioritize_deletion([
        EMPTY_BOARD,
        [[1,2],[4],[]],
    ], [0,2], 3)

    # Should return column with matching number if exists
    assert [1] == prioritize_deletion([
        EMPTY_BOARD,
        [[1,2],[4],[]]
    ], ALL_VIABLE_COLS, 4)

    # Should prioritize greater number of dice if several columns contain matches
    assert [2] == prioritize_deletion([
        EMPTY_BOARD,
        [[2],[],[2,2]]
    ], ALL_VIABLE_COLS, 2)

    # Should return all columns with max matches, if multiple exist
    assert [0,2] == prioritize_deletion([
        EMPTY_BOARD,
        [[2],[1],[2]]
    ], ALL_VIABLE_COLS, 2)