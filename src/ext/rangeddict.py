"""

    rangeddict.py

    Using RBTree, this allows us to use range(#, #) as dictionary keys.

    Use:
    rd = RangedDict()
    rd[(3, 5)] = 12
    print(rd[4])
    : 12

"""

from .rbtree import RedBlueTree


__all__ = ["RangedDict"]


class RangedDict(RedBlueTree):
    """
    By using RBTree, we create a Ranged Dictionary
    """

    _valid_instances = (int, float)

    def __init__(self):
        """
        That which constructs!
        """

        super(RangedDict, self).__init__(
            self.__ranged_dict_comparator, self.__ranged_dict_equals,
            self.__ranged_dict_validator
        )

    def __getitem__(self, key):
        """
        Get Item for RangedDict returns only the first value
        """

        node, _ = self.find_node(key)
        return node._values[0]

    def __ranged_dict_comparator(self, key_one, key_two):
        """
        Compares Key One to Key Two
        Considers Tuple or Int
        """

        if isinstance(key_one, tuple):
            if key_one[1] < key_two[0]:
                return True
            elif key_one[0] > key_two[1]:
                return False
            else:
                raise Exception(
                    f"Overlap! {key_one} already exists in some form!"
                )
        elif isinstance(key_one, self._valid_instances):
            if key_one < key_two[0]:
                return True
            return False
        return None

    def __ranged_dict_equals(self, key_one, key_two):
        """
        Sees if Key One equals Key Two
        Considers Tuple and Int
        """

        if (
            isinstance(key_one, self._valid_instances) and
            key_one >= key_two[0] and key_one <= key_two[1]
        ):
            return True
        elif isinstance(key_one, tuple) and key_one == key_two:
            return True
        return False

    def __ranged_dict_validator(self, key):
        """
        Returns if the given key is valid for our RBTree
        """

        if isinstance(key, tuple):
            for k in key:
                if not isinstance(k, self._valid_instances):
                    return False
            return True
        return False


# We gotta be included!
if __name__ == '__main__':
    pass
