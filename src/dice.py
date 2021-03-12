"""

    Dice.py

    Handles rolling of dice!

"""

# Sys
import array
import math
import random


__all__ = ["Dice"]


class Dice:
    """
    Doice!
    """

    def __init__(self, sides, count):
        """
        Init, how many sides?
        """

        self._sides = sides
        self._count = count

    def __str__(self):
        """
        Gets the String Version of this Dice Roll
        """

        return str(self._count) + "d" + str(self._sides)

    def get_average(self):
        """
        Gets the average for this DiceRoll
        """

        # Average
        average = (((self._sides - 1) / 2) + 1) * self._count

        # Return
        return math.floor(average)

    def get_scaled(self, scale):
        """
        Gets a Scaled version of our Dice
        """

        # Scale set at 0?
        if scale != 0:

            # First, find out which DICE_PROGRESSION we are at.
            for i in range(0, len(DICE_PROGRESSION)):

                # Store the dice
                d = DICE_PROGRESSION[i]

                # This us?
                if d._count == self._count and d._sides == self._sides:

                    # Found us?  Nice!
                    d_scale_index = i + scale

                    # This exist?
                    if d_scale_index < len(DICE_PROGRESSION):

                        # Grab
                        d_scale = DICE_PROGRESSION[d_scale_index]

                        # Return the scaled version!
                        return Dice(d_scale._sides, d_scale._count)

        # Couldn't find or scale, pass a copy of our original.
        return Dice(self._sides, self._count)

    def roll(self, count_to_return=-1, drop_lowest=True):
        """
        Roll them bones!
        """

        # No count?  Set as self.
        if count_to_return == -1:
            count_to_return = self._count

        # Prepared the die range.  Starts at 1, < number_of_sides + 1.
        die_range = range(1, (self._sides + 1))

        # Array of die rolls
        dice_rolls = array.array('I')

        # Perform the rolls, may the odds ever be in your favor!
        for _ in range(0, self._count):
            dice_rolls.insert(0, random.choice(die_range))

        # Start dropping dice!
        while len(dice_rolls) > count_to_return:

            # We want min or max?
            dice_rolls_search = min(dice_rolls)
            if not drop_lowest:
                dice_rolls_search = max(dice_rolls)

            # Now get the first index of the value and remove it!
            dice_rolls.pop(dice_rolls.index(dice_rolls_search))

        # Return it!
        return dice_rolls

    def roll_single(self):
        """
        Rolls and returns a single die roll
        """

        # Array of Dice Rolls
        dice_rolls = self.roll()

        # Just return the first single.
        return dice_rolls[0]

    def roll_sum(
        self, sets_to_roll, maximum=None,
        minimum=None, count_to_return=1,
        drop_lowest=True
    ):
        """
        Builds an array of Dice Rolls, given criteria.
        """

        # Array of Dice Rolls
        dice_rolls = array.array('I')

        # Iterate Dice Rolls
        for _ in range(0, sets_to_roll):

            # Roll the dice!
            dice_rolled = self.roll(count_to_return, drop_lowest)

            # Sum it!
            dice_rolled_sum = sum(dice_rolled)

            # Need to Max/Min?
            if maximum is not None and dice_rolled_sum > maximum:
                dice_rolled_sum = maximum
            elif minimum is not None and dice_rolled_sum < minimum:
                dice_rolled_sum = minimum

            # Insert!
            dice_rolls.insert(0, dice_rolled_sum)

        # Returnnn!
        return dice_rolls

    def roll_sum_list(
        self, sets_to_roll, maximum=None,
        minimum=None, count_to_return=1,
        drop_lowest=True
    ):
        """
        Returns alist of the sum roll
        """

        return self.roll_sum(
            sets_to_roll, maximum, minimum,
            count_to_return, drop_lowest
        ).tolist()

    def roll_sum_single(self):
        """
        We only need a single result?  Just returns the Integer
        """

        # Array of Dice Rolls
        dice_rolls = self.roll_sum(1)

        # Just return the first single.
        return dice_rolls[0]

    def update(self, sides=None, count=None):
        """
        Update our values
        """

        if sides:
            self._sides = sides
        if count:
            self._count = count


# Dice Progression
# Dice					Mean		Max		Min
DICE_PROGRESSION = [
    Dice(4, 1),		# 2.5		4		1
    Dice(2, 2),		# 3			4		2
    Dice(6, 1), 	# 3.5		6		1
    Dice(3, 2),		# 4			6		2
    Dice(8, 1),		# 4.5		8		1
    Dice(4, 2),		# 5			8		2
    Dice(10, 1),    # 5.5		10		1
    Dice(5, 2),		# 6			10		2
    Dice(12, 1),    # 6.5		12		1
    Dice(6, 2),		# 7			12		2
    Dice(4, 3),		# 7.5		12		3
    Dice(8, 2),		# 9			16		2
    Dice(4, 4),		# 10			16		4
    Dice(6, 3),		# 10.5		18		3
    Dice(20, 1),    # 10.5		20		1
    Dice(3, 6)		# 12			18		6
]


# We gotta be included!
if __name__ == '__main__':
    pass
