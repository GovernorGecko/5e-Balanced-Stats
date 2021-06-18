def __str__(self):
        """
        returns:
            str of our stats
        """

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
        """

        return str(self.__stats)

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