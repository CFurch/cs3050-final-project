import arcade


class Room(arcade.Sprite):
    def __init__(self):
        """
        Spawn areas (coordinates for bounding boxes (x, y), list of list of tuples), room type,
        doors, loot_item_spawn_list, wall_list
        """

    def setup(self, room_type, item, x_top_left, y_top_left, spawners, hazards):
        """
        loot_value, allow null for spawners and hazards to be null
        :return:
        """

"""
This class needs a get_walls method to return the walls of the room in the form of a list.
"""


