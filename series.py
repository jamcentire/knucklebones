import numpy

from matches import Match
from players import Player

def run_series(p1: Player, p2: Player, num_games: int = 100):
    overall = [0,0]
    for i in range(num_games):
        # print(f'Running Match {i}...')
        match = Match([p1,p2])
        result = match.run_match()
        overall = numpy.add(overall, result)
        # print(f'Result: {result}   |  Overall: {overall}')
    print('----------------- RESULTS -----------------------')
    p1_win_pctg = overall[0] / (overall[0] + overall[1])
    p2_win_pctg = overall[1] / (overall[0] + overall[1])
    print(f'Overall match score: {overall}')
    print(f'p1 win percentage = {round(p1_win_pctg * 100)}')
    print(f'p2 win percentage = {round(p2_win_pctg * 100)}')
