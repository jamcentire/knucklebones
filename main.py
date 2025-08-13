import numpy

from matches import Match
from players import Player
from heuristics import random_placement, prioritize_multiples

p1 = Player([random_placement])
p2 = Player([prioritize_multiples, random_placement])

SAMPLE_SIZE = 100

overall = [0,0]
for i in range(SAMPLE_SIZE):
    print(f'Running Match {i}...')
    match = Match([p1,p2])
    result = match.run_match()
    overall = numpy.add(overall, result)
    print(f'Result: {result}   |  Overall: {overall}')
print('----------------- RESULTS -----------------------')
print(overall)