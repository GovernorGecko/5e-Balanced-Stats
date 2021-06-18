"""
    balancedstats.py

    Balanced Stats is used to create Balanced Stat arrays.

    We consider base stats to be all 8s with 27 starting points

    Given the standard array and point buy mechanics of DnD 5e,
    can create either a set of balanced, or unbalanced stats.
    It'll keep its place in points, so these can be called multiple
    times to really randomize the sets of stats.

    Stat Rules:

    Rolling:
    4 six sided dice, drop the lowest

    Standard Array:
    15, 14, 13, 12, 10, 8

    Point Buy:
    Every stat starts at 8, with 27 points to spend.

    Buying 9 - 13 is 1 point
    Buying 14 or 15 is 2 points

    DnD 4e rules:
    Buying 16 or 17 is 3 points
    Buying 18 is 4 points

    Extra rules (homebrew)
    Buying below < 8 costs 1 point
"""

import math
import random

from .Dice.src.dice import Dice
from .RangedDict.src.rangeddict import RangedDict


class BalancedStats:
    """
    parameters:
        Dice our dice to roll for each stat
        int how many lowest dice to drop each roll
        int maximum sum roll to accept as a stat
        int minimum sum roll to accept as a stat
        int points we can spend
        list of ints of our base stats
        list of strings of our stat order
    """

    # Point Weight Dict
    __POINT_WEIGHT_DICT = RangedDict()
    __POINT_WEIGHT_DICT[(4, 13)] = 1
    __POINT_WEIGHT_DICT[(14, 15)] = 2
    __POINT_WEIGHT_DICT[(16, 17)] = 3
    __POINT_WEIGHT_DICT[(18, 18)] = 4
    __POINT_WEIGHT_DICT[(19, 30)] = 100

    __slots__ = [
        "__base_stats", "__dice", "__lowest_to_drop", "__maximum_stat",
        "__minimum_stat", "__points_to_spend", "__stats", "__stats_order"
    ]

    def __init__(
        self, dice=Dice(6, 4), lowest_to_drop=1,
        maximum_stat=18, minimum_stat=3, points_to_spend=27,
        base_stats=[8, 8, 8, 8, 8, 8],
        stats_order=[
            "STRENGTH", "DEXTERITY", "CONSTITUTION",
            "INTELLIGENCE", "WISDOM", "CHARISMA"
        ]
    ):

        # Error Check
        if not isinstance(dice, Dice):
            raise ValueError("Dice must be an instance of Dice.")
        elif (
            not isinstance(lowest_to_drop, int) or
            lowest_to_drop < 0
        ):
            raise ValueError("Lowest Dice to Drop must be an int and >= 0.")
        elif(
            not isinstance(maximum_stat, int) or
            not isinstance(minimum_stat, int) or
            maximum_stat < minimum_stat
        ):
            raise ValueError(
                "Maximum/Minimum must be ints and maximum > minimum."
            )
        elif(
            not isinstance(points_to_spend, int)
        ):
            raise ValueError(
                "Points to Spend must be an int."
            )
        elif(
            not isinstance(base_stats, list) or
            not isinstance(stats_order, list) or
            len(base_stats) != len(stats_order)
        ):
            raise ValueError(
                "Stats and Stats Order must be lists of the same length."
            )
        elif(
            not all(isinstance(i, int) for i in base_stats)
        ):
            raise ValueError(
                "Base Stats must be a list of integers."
            )
        elif(
            not all(isinstance(i, str) for i in stats_order)
        ):
            raise ValueError(
                "Stats Order must be a list of strings."
            )

        # Set to Default Settings
        self.__base_stats = base_stats
        self.__dice = dice
        self.__lowest_to_drop = lowest_to_drop
        self.__maximum_stat = maximum_stat
        self.__minimum_stat = minimum_stat
        self.__points_to_spend = points_to_spend
        self.__stats = base_stats
        self.__stats_order = stats_order

    def __str__(self):
        """
        returns:
            str print out of our current stats
        """

        return(
            "".join(
                f'{self.__stats_order[i][0:3]} '
                f'{self.__stats[i]} '
                for i in range(0, len(self.__stats_order))
            )
        )

    def get_stat_lowest(self):
        """
        returns:
            str of our lowest stat
        """

        return self.__stats_order[
            self.__stats.index(min(self.__stats))
        ]
