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
        int maximum sum roll to accept as a stat
        int minimum sum roll to accept as a stat
        int points we can spend
        list of ints of our base stats
        list of strings of our stat order
    """

    # Point Weight
    __POINT_WEIGHT_DICT = RangedDict()
    __POINT_WEIGHT_DICT[(3, 13)] = 1
    __POINT_WEIGHT_DICT[(14, 15)] = 2
    __POINT_WEIGHT_DICT[(16, 17)] = 3
    __POINT_WEIGHT_DICT[(18, 18)] = 4
    __POINT_WEIGHT_MINIMUM = 3
    __POINT_WEIGHT_MAXIMUM = 18

    __slots__ = [
        "__base_points", "__base_stats", "__dice", "__lowest_to_drop",
        "__maximum_stat", "__minimum_stat", "__points_spent",
        "__stats", "__stats_order"
    ]

    def __init__(
        self, dice_count=4, maximum_stat=18, minimum_stat=3,
        base_points=27, base_stats=[8, 8, 8, 8, 8, 8],
        stats_order=[
            "STRENGTH", "DEXTERITY", "CONSTITUTION",
            "INTELLIGENCE", "WISDOM", "CHARISMA"
        ]
    ):

        # Error Check
        if (
            not isinstance(dice_count, int) or
            dice_count < 3
        ):
            raise ValueError("Dice count must be an int >= 3.")
        elif(
            not isinstance(maximum_stat, int) or
            not isinstance(minimum_stat, int) or
            maximum_stat < minimum_stat or
            maximum_stat > self.__POINT_WEIGHT_MAXIMUM or
            minimum_stat < self.__POINT_WEIGHT_MINIMUM
        ):
            raise ValueError(
                f"Maximum/Minimum must be ints and maximum > minimum and "
                f"between {self.__POINT_WEIGHT_MINIMUM} and "
                f"{self.__POINT_WEIGHT_MAXIMUM}"
            )
        elif(
            not isinstance(base_points, int)
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
        self.__base_points = base_points
        self.__base_stats = base_stats
        self.__dice = Dice(6, dice_count)
        self.__lowest_to_drop = dice_count - 3
        self.__maximum_stat = maximum_stat
        self.__minimum_stat = minimum_stat
        self.__points_spent = 0
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

    def __validate_stat(self, stat):
        """
        parameters:
            str of stat to ensure we have
        """
        if stat not in self.__stats_order:
            raise ValueError(
                f"{stat} not found in {self.__stats_order}"
            )

    def create_balanced_stats(self):
        """
        Sets our stats to a balanced set of stats.
        """

        self.create_unbalanced_stats()

        while self.__points_spent != 0:



    def create_unbalanced_stats(self):
        """
        Sets our stats to an unbalanced set of stats.
        """

        self.__points_spent = 0
        self.__stats = []

        for i in range(0, len(self.__stats_order)):
            self.__stats.append(
                self.__dice.roll_sum_with_culling(
                    self.__minimum_stat,
                    self.__maximum_stat,
                    self.__lowest_to_drop
                )
            )
            self.__points_spent -= self.get_point_cost(
                self.__base_stats[i],
                self.__stats[i]
            )

    def get_point_cost(self, start, end):
        """
        parameters:
            int start stat value
            int end stat value
        returns:
            int of point cost
        """

        # Error checking.
        if (
            not isinstance(start, int) or
            not isinstance(end, int) or
            min(start, end) < self.__POINT_WEIGHT_MINIMUM or
            max(start, end) > self.__POINT_WEIGHT_MAXIMUM
        ):
            raise ValueError(
                f"Start/End must be ints and between "
                f"{self.__POINT_WEIGHT_MINIMUM} and "
                f"{self.__POINT_WEIGHT_MAXIMUM}"
            )

        # Point cost between two numbers is the same no matter
        # what.  So it is easiest to start at our higher number
        # and go to the lower.  We then add each number cost up.
        point_cost = 0
        for i in range(
            max(start, end),
            min(start, end),
            -1
        ):
            point_cost += self.__POINT_WEIGHT_DICT[i]

        # If we are increasing stats, we have to spend points.
        if start < end:
            point_cost *= -1

        return point_cost

    def get_points_left(self):
        """
        returns:
            int of points remaining to spend
        """
        return self.__base_points - self.__points_spent

    def get_stats(self):
        """
        returns:
            list of our stats
        """
        return self.__stats

    def get_stat_lowest(self):
        """
        returns:
            str of our lowest stat
        """
        return self.__stats_order[
            self.__stats.index(min(self.__stats))
        ]

    def get_stat_bonus(self, stat):
        """
        parameters:
            str stat name in our stat order
        returns:
            int bonus of this stat
        """

        self.__validate_stat(stat)

        return math.floor((self.get_stat_value(stat) - 10) / 2)

    def get_stat_detail(self, stat):
        """
        parameters:
            str stat name in our stat order
        returns:
            str representation of our stat
        """

        self.__validate_stat(stat)

        return (
            f"{stat[0:3]} "
            f"{self.get_stat_value(stat)} "
            f"({self.get_stat_bonus(stat)})"
        )

    def get_stat_value(self, stat):
        """
        parameters:
            str stat name in our stat order
        returns:
            int stat value
        """

        self.__validate_stat(stat)

        return self.__stats[self.__stats_order.index(stat)]
