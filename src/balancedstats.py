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
    3+ six sided dice, drop the lowest

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
    Buying below 8 costs 1 point
"""

import math
import random

from .Dice.src.dice import Dice
from .RangedDict.src.rangeddict import RangedDict


class BalancedStats:
    """
    parameters:
        (optional)
        int lowest number of dice to drop
        int maximum sum roll to accept as a stat
        int minimum sum roll to accept as a stat
        int of extra points to spend
        list of ints for starting stats if you wish to not use the
            standard 8s with 27 points to spend.  Instead it'll calculate
            points off the given stats and set to spend to 0.
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
        "__dice", "__lowest_dice_count", "__maximum_stat", "__minimum_stat",
        "__points_remaining", "__stats", "__stats_order"
    ]

    def __init__(
        self, lowest_dice_count=1, maximum_stat=18, minimum_stat=3,
        extra_points=0, stats=None, stats_order=[
            "STRENGTH", "CONSTITUTION", "DEXTERITY",
            "INTELLIGENCE", "WISDOM", "CHARISMA"
        ]
    ):

        # Error Check
        if (
            not isinstance(lowest_dice_count, int) or
            lowest_dice_count < 0
        ):
            raise ValueError("Lowest Dice Count must be an int >= 0.")
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
            stats is not None and (
                not isinstance(stats, list) or
                not isinstance(stats_order, list) or
                len(stats) != len(stats_order)
            )
        ):
            raise ValueError(
                "Stats and Stats Order must be lists of the same length."
            )
        elif(
            stats is not None and
            not all(isinstance(i, int) for i in stats)
        ):
            raise ValueError(
                "Base Stats must be a list of integers."
            )
        elif(
            not isinstance(stats_order, list) or
            not all(isinstance(i, str) for i in stats_order)
        ):
            raise ValueError(
                "Stats Order must be a list of strings."
            )

        # Set to Default Settings
        self.__dice = Dice(6, 3 + lowest_dice_count)
        self.__lowest_dice_count = lowest_dice_count
        self.__maximum_stat = maximum_stat
        self.__minimum_stat = minimum_stat
        self.__stats_order = stats_order

        # Calculate points remaining
        if stats is None:
            self.__points_remaining = 27 + extra_points
            self.__stats = [8] * len(stats_order)
            self.set_stats_to_value(minimum_stat)
        else:
            self.__points_remaining = 0
            self.__stats = stats

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

    def create_balanced_stats(self):
        """
        Sets our stats to a balanced set of stats.
        """

        self.create_unbalanced_stats()

        # Working our way down to 0!
        while self.__points_remaining != 0:

            # Randomly pick a stat
            random_stat = random.choice(self.__stats_order)

            # What value do we want to buy?
            value_to_buy = self.get_stat_value(random_stat)
            if self.__points_remaining > 0:
                value_to_buy += 1
            else:
                value_to_buy -= 1

            # Update our stat.
            self.set_stat(random_stat, value_to_buy)

    def create_unbalanced_stats(self):
        """
        Sets our stats to an unbalanced set of stats.
        """

        for stat in self.__stats_order:
            self.set_stat(
                stat,
                self.__dice.roll_sum_with_culling(
                    self.__minimum_stat,
                    self.__maximum_stat,
                    self.__lowest_dice_count
                )
            )

    def get_point_cost(self, start, end):
        """
        parameters:
            int start stat value
            int end stat value
        returns:
            int of point cost, negative if we have to spend points
            positive if we get poitns back.
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

        # Return!
        return point_cost

    def get_points_left(self):
        """
        returns:
            int of points remaining to spend
        """
        return self.__points_remaining

    def get_stat_bonus(self, stat):
        """
        parameters:
            str stat name in our stat order
        returns:
            int bonus of this stat
        """

        index = self.get_stat_index(stat)

        return math.floor((self.__stats[index] - 10) / 2)

    def get_stat_detail(self, stat):
        """
        parameters:
            str stat name in our stat order
        returns:
            str representation of our stat
        """

        return (
            f"{stat[0:3]} "
            f"{self.get_stat_value(stat)} "
            f"({self.get_stat_bonus(stat)})"
        )

    def get_stat_index(self, stat):
        """
        parameters:
            str stat name in our stat order
        returns:
            int index of the stat in stat order
        """

        if stat not in self.__stats_order:
            raise ValueError(
                f"{stat} not found in {self.__stats_order}"
            )
        else:
            return self.__stats_order.index(stat)

    def get_stat_lowest(self):
        """
        returns:
            str of our lowest stat
        """
        return self.__stats_order[
            self.__stats.index(min(self.__stats))
        ]

    def get_stat_value(self, stat):
        """
        parameters:
            str stat name in our stat order
        returns:
            int stat value
        """

        index = self.get_stat_index(stat)

        return self.__stats[index]

    def get_stats(self):
        """
        returns:
            list of our stats
        """
        return self.__stats

    def get_stats_sorted(self, reversed=True):
        """
        parameters:
            bool if we should reverse the sort list
        """
        stats_sorted = self.__stats
        stats_sorted.sort(reverse=reversed)
        return stats_sorted

    def set_stat(self, stat, value):
        """
        Sets the given stat to the given value.  This updates our
        points remaining.
        paramaters:
            str/int stat name/index in our stat order
            int value to set the stat to
        """

        # Error Checking
        if not isinstance(value, int):
            raise ValueError("Value must be an int")
        elif(
            value > self.__maximum_stat or
            value < self.__minimum_stat
        ):
            return

        # Index of the stat in our order.
        index = self.get_stat_index(stat)

        # Update the points remaining and stat.
        self.__points_remaining += self.get_point_cost(
            self.__stats[index], value
        )
        self.__stats[index] = value

    def set_stats_to_value(self, value):
        """
        paramaters:
            int value to set to.
        """

        # Value an int?
        if not isinstance(value, int):
            raise ValueError("Value must be an int.")

        # Iterate!
        for stat in self.__stats_order:
            self.set_stat(stat, value)
