import arcade


class Room(arcade.Sprite):
    def __init__(self):
        """
        Spawn areas (coordinates for bounding boxes (x, y), list of list of tuples), room type,
        doors, loot_item_spawn_list, wall_list
        """

    def setup(self, bitwise_repr, room_type, x_center, y_center, loot_to_spawn, spawners, hazards):
        """
        loot_value, allow null for spawners and hazards to be null
        :return:
        """

"""
This class needs a get_walls method to return the walls of the room in the form of a list.
"""


