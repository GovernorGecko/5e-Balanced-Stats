"""
    _test.py
"""

import math

from src.balancedstats import BalancedStats

# Simple Balanced Stats
simple_bs = BalancedStats()
simple_bs.create_balanced_stats()
print(simple_bs)
print(simple_bs.get_stats_sorted())

# Simple Balanced Stats, providing a stat set.
# This can be useful, considering players typically start
# at 8 on all stats and are given 27 to spend.  With this,
# you could balance the stats of a monster or something which
# has fewer points to spend.
simple_bs_w_stats = BalancedStats(stats=[12, 11, 10, 9, 8, 7])
simple_bs_w_stats.create_balanced_stats()
print(simple_bs_w_stats)

# Rolling for stats on average does produce better stats
# but by how much?  The below rolls stats 1000 times and
# gets the average of how much it'd cost in points (past
# what we are given) to buy to the rolls.
points_required = 0
for i in range(0, 1000):
    ubs = BalancedStats()
    ubs.create_unbalanced_stats()
    points_required += ubs.get_points_left()
points_required /= 1000
print(points_required)

# Balanced Stats with average points required
average_bs = BalancedStats(extra_points=abs(math.floor(points_required)))
average_bs.create_balanced_stats()
print(average_bs)
