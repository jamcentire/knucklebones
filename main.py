from players import Player
from heuristics import random_placement, prioritize_multiples, prioritize_deletion
from series import run_series

p_prio = Player([prioritize_multiples, random_placement])
p_del = Player([prioritize_deletion, random_placement])
p_rand = Player([random_placement])

run_series(p_prio, p_del, 10000)