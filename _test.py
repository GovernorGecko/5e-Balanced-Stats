"""

    natural_stats.py

    Calls our Balanced Stats, getting properly balanced array of stats.

"""

# Moinnne
from src.balancedstats import BalancedStats


# Constants
constants = {}
constants["DICE TO RETURN"] = 3
constants["DICE TO ROLL"] = 4
constants["DICE SIDES"] = 6
constants["MAXIMUM STAT"] = 18
constants["MINIMUM STAT"] = 6
constants["POINTS TO SPEND"] = 27
constants["RANDOM TRIES"] = 100
constants["STARTING STATS"] = [8, 8, 8, 8, 8, 8]

# Print Constants
print(constants)

# Balanced Stats Initialized
balanced_stats = BalancedStats()
"""
balanced_stats.update_settings(
    points_to_spend=constants["POINTS TO SPEND"],
    dice_sides=constants["DICE SIDES"],
    dice_to_roll=constants["DICE TO ROLL"],
    dice_to_return=constants["DICE TO RETURN"],
    maximum_stat=constants["MAXIMUM STAT"],
    minimum_stat=constants["MINIMUM STAT"]
   )
balanced_stats.set_stats_from_list(constants["STARTING STATS"])
"""

# Balanced Stats, Set Stats
for _ in range(0, 5):
    balanced_stats.create_balanced_stats()
    print(balanced_stats)
    balanced_stats.revert_stats_list(constants["STARTING STATS"])

# Balanced Stats, Don't Set Stats
for _ in range(0, 5):
    balanced_stats.create_balanced_stats()
    print(balanced_stats.get_stats_list_sorted())
    balanced_stats.revert_stats_list(constants["STARTING STATS"])

# Average time!
points_left_over = 0
for _ in range(0, constants["RANDOM TRIES"]):
    balanced_stats.create_unbalanced_stats()
    points_left_over = points_left_over + balanced_stats.get_points_left()
    balanced_stats.revert_stats_list(constants["STARTING STATS"])
print(points_left_over / constants["RANDOM TRIES"])
