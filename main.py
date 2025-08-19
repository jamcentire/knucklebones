from players import Player
from heuristics import random_placement, prioritize_multiples, prioritize_deletion
from series import run_series

p_mult = Player([prioritize_multiples, random_placement])
p_del = Player([prioritize_deletion, random_placement])
p_rand = Player([random_placement])
p_rand2 = Player([random_placement])

run_series(p_del, p_mult, 10000)