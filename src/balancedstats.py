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

# Sys
from enum import Enum
import math
import random

# Mines
from .dice import Dice
from .ext.rangeddict import RangedDict


__all__ = ["BalancedStats"]


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
    """

    # Initial Defines
    DICE_SIDES = 6
    DICE_TO_ROLL = 4
    DICE_TO_RETURN = 3
    MAXIMUM_STAT = 18
    MINIMUM_STAT = 3
    POINTS_TO_SPEND = 27
    STARTING_STATS = [8, 8, 8, 8, 8, 8]

    # Point Weight Dict
    POINT_WEIGHT_DICT = RangedDict()
    POINT_WEIGHT_DICT[(4, 13)] = 1
    POINT_WEIGHT_DICT[(14, 15)] = 2
    POINT_WEIGHT_DICT[(16, 17)] = 3
    POINT_WEIGHT_DICT[(18, 18)] = 4
    POINT_WEIGHT_DICT[(19, 30)] = 100

    def __init__(self, StatsEnum=BalancedStatsEnum):
        """
        Constructor!
        """

        # Set to Default Settings
        self.update_settings()

        # Our Stats
        self._stats = {}
        self._stat_order = [
            StatsEnum.STRENGTH,
            StatsEnum.DEXTERITY,
            StatsEnum.CONSTITUTION,
            StatsEnum.INTELLIGENCE,
            StatsEnum.WISDOM,
            StatsEnum.CHARISMA
           ]
        self.set_stats_from_list(self.STARTING_STATS)

    def __str__(self):
        """
        Gets our stats as a string
        """

        # Headers
        headers = "".join(
            [f'{stat.name[:3]:^10s}' for stat in self._stats.keys()]
        )

        # Values
        values = "".join(
            [
                f'{self.get_stat_bonus_string(stat):^10s}'
                for stat, value in self._stats.items()
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
        while self._points_left != 0:

            # Randomly pick a stat
            random_stat = random.choice(self._stat_order)

            # Iteration and Increment, defaulting to having
            # extra points to spend
            iteration = 1
            increment = True

            # Do we not have extra points?  Need to decrement
            if self._points_left < 0:
                iteration = -1
                increment = False

            # How many points do we plan to spend?
            points_available = self.get_point_weight(
                self._stats[random_stat], increment
            )

            # Spend it!
            if points_available:
                self._stats[random_stat] = self._stats[random_stat] + iteration
                self._points_left = self._points_left + points_available

    def create_unbalanced_stats(self):
        """
        Creates a set of unbalanced stats, returning the
        extra points and stats.
        """

        # Get them sterts!
        unbalanced_stats = self._dice.roll_sum_list(
            6, self._maximum_stat,
            self._minimum_stat, self._dice_to_return
        )

        # Rolls have been completed!  Now we need to figure out
        # how many points over or under we are.
        for stat in range(0, len(unbalanced_stats)):
            self._points_left = self._points_left - self.get_point_weight_diff(
                unbalanced_stats[stat], self._stats[self._stat_order[stat]]
            )

        # Set Stats
        self.set_stats_from_list(unbalanced_stats)

    def get_lowest_stat(self):
        """
        Gets our Lowest Stat
        """

        lowest_stat = BalancedStatsEnum.STRENGTH
        for stat in self._stat_order:
            if self._stats[stat] < self._stats[lowest_stat]:
                lowest_stat = stat
        return lowest_stat

    def get_point_weight(self, initial, increment=False):
        """
        Gets the difference in points when moving between two values.
        """

        # Going up?  Returning a negative from the next value up.
        if (
            increment and (initial + 1) <= self._maximum_stat and
            self.POINT_WEIGHT_DICT.find_node(initial + 1)
        ):
            return self.POINT_WEIGHT_DICT[initial + 1] * -1

        # Going down? Return a positive.
        elif (
            not increment and (initial - 1) >= self._minimum_stat and
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

        return self._points_left

    def get_stat(self, stat):
        """
        Gets a Stat
        """

        if stat in BalancedStatsEnum:
            return self._stats[stat]
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

        return list(self._stats.values())

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
        for i in range(0, len(self._stat_order)):

            # Get our Stat, Current and Desired Value
            stat = self._stat_order[i]
            stat_current_value = self._stats[stat]
            stat_desired_value = list_of_stats[i]

            # Was the set successful?  If so, update our points to spend
            if self.set_stat(stat, stat_desired_value):
                self._points_left += self.get_point_weight_diff(
                    stat_current_value, stat_desired_value
                )

    def set_stat(self, stat, value):
        """
        Given a stat and value, update it
        """

        # Is this stat value in the allowed range?
        if value in range(self._minimum_stat, self._maximum_stat + 1):
            self._stats[stat] = value
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
            self.set_stat(self._stat_order[i], list_of_stats[i])

    def update_settings(
        self,
        points_to_spend=POINTS_TO_SPEND,
        dice_sides=DICE_SIDES,
        dice_to_roll=DICE_TO_ROLL,
        dice_to_return=DICE_TO_RETURN,
        maximum_stat=MAXIMUM_STAT,
        minimum_stat=MINIMUM_STAT
       ):
        """
        Update our settings, will default those not passed.
        """

        # Set PtS, Dice, and DtR.... ACRONYMS
        self._points_left = points_to_spend
        self._dice = Dice(dice_sides, dice_to_roll)
        self._dice_to_return = dice_to_return

        # Maximum and Minimum
        self._maximum_stat = maximum_stat
        if minimum_stat <= maximum_stat:
            self._minimum_stat = minimum_stat


# We gotta be included!
if __name__ == '__main__':
    pass
