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

from enum import Enum
import math
import random

from .Dice.src.dice import Dice
from .RangedDict.src.rangeddict import RangedDict


class BalancedStatsEnum(Enum):
    """
    Simple Stats Enum, can be overwritten
    by a custom one so long as the names stay
    the same.
    """

    STRENGTH = 0
    DEXTERITY = 1
    CONSTITUTION = 2
    INTELLIGENCE = 3
    WISDOM = 4
    CHARISMA = 5


class BalancedStats:
    """
    Balanced Stats
    parameters:
        Enum following BalancedStatsEnum
    """

    # Point Weight Dict
    POINT_WEIGHT_DICT = RangedDict()
    POINT_WEIGHT_DICT[(4, 13)] = 1
    POINT_WEIGHT_DICT[(14, 15)] = 2
    POINT_WEIGHT_DICT[(16, 17)] = 3
    POINT_WEIGHT_DICT[(18, 18)] = 4
    POINT_WEIGHT_DICT[(19, 30)] = 100

    __slots__ = [
        "__dice", "__lowest_to_drop", "__maximum_stat", "__minimum_stat",
        "__points_to_spend", "__stats", "__stat_order"
    ]

    def __init__(
        self, dice=Dice(6, 4), lowest_to_drop=1,
        maximum_stat=18, minimum_stat=3, points_to_spend=27,
        starting_stats=[8, 8, 8, 8, 8, 8], stats_enum=BalancedStatsEnum
    ):

        # Error Check
        if not isinstance(dice, Dice):
            raise ValueError("Dice must be an instance of Dice.")
        elif (
            not isinstance(lowest_to_drop, int) or
            lowest_to_drop < 0
        ):
            raise ValueError("Lowest Dice to Drop must be an int and > 0.")
        elif(
            not isinstance(maximum_stat, int) or
            not isinstance(minimum_stat, int) or
            maximum_stat < minimum_stat
        ):
            raise ValueError(
                "Maximum/Minimum must be ints and maximum > minimum."
            )

        # Set to Default Settings
        self.__dice = dice
        self.__lowest_to_drop = lowest_to_drop
        self.__maximum_stat = maximum_stat
        self.__minimum_stat = minimum_stat
        self.__points_to_spend = points_to_spend

        # Our Stats
        self.__stats = {}
        self.__stat_order = [
            stats_enum.STRENGTH,
            stats_enum.DEXTERITY,
            stats_enum.CONSTITUTION,
            stats_enum.INTELLIGENCE,
            stats_enum.WISDOM,
            stats_enum.CHARISMA
           ]
        self.set_stats_from_list(starting_stats)

    def __str__(self):
        """
        returns:
            str of our stats
        """

        # Headers
        headers = "".join(
            [f'{stat.name[:3]:^10s}' for stat in self.__stats.keys()]
        )

        # Values
        values = "".join(
            [
                f'{self.get_stat_bonus_string(stat):^10s}'
                for stat in self.__stats.keys()
            ]
        )

        # Return!
        return f"\n{headers}\n{values}"

    def create_balanced_stats(self):
        """
        Creates a set of balanced stats
        """

        # First, we need an unbalanced version of our stats
        self.create_unbalanced_stats()

        # Now, we need to make it better!
        # Gotta get to 0 points!
        while self.__points_to_spend != 0:

            # Randomly pick a stat
            random_stat = random.choice(self.__stat_order)

            # Iteration and Increment, defaulting to having
            # extra points to spend
            iteration = 1
            increment = True

            # Do we not have extra points?  Need to decrement
            if self.__points_to_spend < 0:
                iteration = -1
                increment = False

            # How many points do we plan to spend?
            points_available = self.get_point_weight(
                self.__stats[random_stat], increment
            )

            # Spend it!
            if points_available:
                self.__stats[random_stat] = self.__stats[random_stat] + iteration
                self.__points_to_spend = self.__points_to_spend + points_available

    def create_unbalanced_stats(self):
        """
        Creates a set of unbalanced stats, returning the
        extra points and stats.
        """

        # Get them sterts!
        unbalanced_stats = []
        for _ in range(0, 6):
            unbalanced_stats.append(
                self.__dice.roll_sum_with_culling(
                    self.__minimum_stat, self.__maximum_stat, 1
                )
            )

        # Rolls have been completed!  Now we need to figure out
        # how many points over or under we are.
        for stat in range(0, len(unbalanced_stats)):
            self.__points_to_spend = self.__points_to_spend - self.get_point_weight_diff(
                unbalanced_stats[stat], self.__stats[self.__stat_order[stat]]
            )

        # Set Stats
        self.set_stats_from_list(unbalanced_stats)

    def get_lowest_stat(self):
        """
        Gets our Lowest Stat
        """

        lowest_stat = BalancedStatsEnum.STRENGTH
        for stat in self.__stat_order:
            if self.__stats[stat] < self.__stats[lowest_stat]:
                lowest_stat = stat
        return lowest_stat

    def get_point_weight(self, initial, increment=False):
        """
        Gets the difference in points when moving between two values.
        """

        # Going up?  Returning a negative from the next value up.
        if (
            increment and (initial + 1) <= self.__maximum_stat and
            self.POINT_WEIGHT_DICT.find_node(initial + 1)
        ):
            return self.POINT_WEIGHT_DICT[initial + 1] * -1

        # Going down? Return a positive.
        elif (
            not increment and (initial - 1) >= self.__minimum_stat and
            self.POINT_WEIGHT_DICT.find_node(initial)
        ):
            return self.POINT_WEIGHT_DICT[initial]

        # Not in our range?
        else:
            return 0

    def get_point_weight_diff(self, initial, final):
        """
        Given two different values, calls GetPointWeight to figure out
        the total points we need to move from initial to final.
        """

        # Our Point Weight to return
        point_weight = 0

        # Iteration and Increment.
        # If our initial is greater than our new value,
        # Need to decrement through the stat.
        if initial > final:
            iteration = -1
            increment = False
        else:
            iteration = 1
            increment = True

        # Iterate!
        for i in range(initial, final, iteration):
            point_weight = point_weight + self.get_point_weight(i, increment)

        # Return!
        return point_weight

    def get_points_left(self):
        """
        Returns how many points we have remaining
        to spend.
        """

        return self.__points_to_spend

    def get_stat(self, stat):
        """
        Gets a Stat
        """

        if stat in BalancedStatsEnum:
            return self.__stats[stat]
        else:
            return 0

    def get_stat_bonus(self, stat):
        """
        Gets our Stat Bonus, given a Stat
        """

        stat_value = self.get_stat(stat)
        if stat_value >= 12 or stat_value <= 9:
            return math.floor((stat_value - 10) / 2)
        return 0

    def get_stat_bonus_string(self, stat):
        """
        Gets a Stat Bonus, as a String
        """
        stat_bonus = self.get_stat_bonus(stat)
        return f"{self.get_stat(stat)} ({stat_bonus})"

    def get_stats_list(self):
        """
        Gets our stats as a list
        """

        return list(self.__stats.values())

    def get_stats_list_sorted(self, reversed=True):
        """
        Gets our stats as a list, sorted
        """

        list_of_stats = self.get_stats_list()
        list_of_stats.sort(reverse=reversed)
        return list_of_stats

    def revert_stats(self, value):
        """
        Given a number, reduces stats to it, returning points.
        """
        self.revert_stats_list([value, value, value, value, value, value])

    def revert_stats_list(self, list_of_stats):
        """
        Given a list of stats, reduces stats to it, returning points.
        """

        # Iterate, getting points back
        for i in range(0, len(self.__stat_order)):

            # Get our Stat, Current and Desired Value
            stat = self.__stat_order[i]
            stat_current_value = self.__stats[stat]
            stat_desired_value = list_of_stats[i]

            # Was the set successful?  If so, update our points to spend
            if self.set_stat(stat, stat_desired_value):
                self.__points_to_spend += self.get_point_weight_diff(
                    stat_current_value, stat_desired_value
                )

    def set_stat(self, stat, value):
        """
        Given a stat and value, update it
        """

        # Is this stat value in the allowed range?
        if value in range(self.__minimum_stat, self.__maximum_stat + 1):
            self.__stats[stat] = value
            return True

        # Couldn't do it.
        return False

    def set_stats_from_list(self, list_of_stats):
        """
        Given a list, sets our stats.
        """

        # Enough vars?
        if len(list_of_stats) < 6:
            return False

        # Set
        for i in range(0, 6):
            self.set_stat(self.__stat_order[i], list_of_stats[i])
