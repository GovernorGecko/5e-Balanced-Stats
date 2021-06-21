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