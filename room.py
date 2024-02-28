import arcade


class Room(arcade.Sprite):
    def __init__(self):
        """
        Spawn areas (coordinates for bounding boxes (x, y), list of list of tuples), room type,
        doors, loot_item_spawn_list, wall_list
        """
        self.wall_list = None
        self.loot_item_spawn_list = None
        self.spawners = None
        self.room_type = None
        self.doors = None
        self.x_center = None
        self.y_center = None
        self.hazards = None
        self.spawners = None

    def setup(self, room_type, item, x_center, y_center, spawners=None, hazards=None, loot_item_spawn_list = None):
        """
        loot_value, allow null for spawners and hazards to be null
        :return:
        """
        self.wall_list = arcade.SpriteList()

        self.loot_item_spawn_list = loot_item_spawn_list
        self.spawners = spawners
        self.hazards = hazards
        self.room_type = room_type
        self.x_center = x_center
        self.y_center = y_center
        self.width = 2560
        self.height = 1440
    def get_walls():
        return self.wall_list

"""
This class needs a get_walls method to return the walls of the room in the form of a list.
"""

"""
TO DO: Getters and Setters for all values
"""



