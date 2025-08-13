from heuristics import prioritize_multiples, prioritize_deletion
# TODO change naming conventions
from constants import NUM_COLUMNS

EMPTY_BOARD = [[] for i in range(NUM_COLUMNS)]

def test_prioritize_multiples_heuristic():
    # Should return -1 if no match found
    assert -1 == prioritize_multiples([
        [[1,2],[4],[]],
        EMPTY_BOARD,
    ], 5)

    # Should return column with matching number if exists
    assert 1 == prioritize_multiples([
        [[1,2],[4],[]],
        EMPTY_BOARD
    ], 4)

    # Should return -1 if matches only exist in full columns
    assert -1 == prioritize_multiples([
        [[1,2],[],[4,5,6]],
        EMPTY_BOARD
    ], 5)

    # Should prioritize greater number of multiples if several columns contain matches
    assert 2 == prioritize_multiples([
        [[2],[],[2,2]],
        EMPTY_BOARD
    ], 2)

    # Should choose leftmost column if several columns contain matches
    # TODO should it? Seems restrictive
    assert 0 == prioritize_multiples([
        [[2],[1],[2]],
        EMPTY_BOARD
    ], 2)


def test_prioritize_deletion_heuristic():
    # Should return -1 if no match found
    assert -1 == prioritize_deletion([
        EMPTY_BOARD,
        [[1,2],[4],[]],
    ], 3)

    # Should return column with matching number if exists
    assert 1 == prioritize_deletion([
        EMPTY_BOARD,
        [[1,2],[4],[]]
    ], 4)

    # Should return -1 if matches only exist in full columns
    assert -1 == prioritize_deletion([
        [[],[],[1,1,1]],
        [[],[],[5]]
    ], 5)

    # Should prioritize greater number of multiples if several columns contain matches
    assert 2 == prioritize_deletion([
        EMPTY_BOARD,
        [[2],[],[2,2]]
    ], 2)

    # Should choose leftmost column if several columns contain matches
    # TODO should it? Seems restrictive
    assert 0 == prioritize_deletion([
        EMPTY_BOARD,
        [[2],[1],[2]]
    ], 2)