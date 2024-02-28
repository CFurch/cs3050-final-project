import json

import arcade


# Update this based on tile size
TILE_SIZE = 128


class Room(arcade.Sprite):
    def __init__(self):
        """
        representation of room, pull from json,
        """
        super().__init__()
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

        self.wall_list = arcade.SpriteList()

        # Load room data from JSON file
        with open("rooms.json") as f:
            rooms_data = json.load(f)

        # Get walls data based on room type
        walls_data = rooms_data["rooms"].get(room_type, {}).get("walls", [])

        # Create walls based on walls data
        for wall_data in walls_data:
            center_x = wall_data["center_x"] + self.x_center - TILE_SIZE
            center_y = wall_data["center_y"] + self.y_center - TILE_SIZE
            width = wall_data["width"]
            height = wall_data["height"]
            self.create_wall(center_x, center_y, width, height)

    def create_wall(self, center_x, center_y, width, height):
        """
        Need to adapt this function for the texture of each wall (assuming base texture for now,
           loaded using the room type)
        :param center_x:
        :param center_y:
        :param width:
        :param height:
        :return:
        """
        wall = arcade.SpriteSolidColor(width, height, arcade.csscolor.GRAY)
        wall.center_x = center_x
        wall.center_y = center_y
        self.wall_list.append(wall)

    def get_walls(self):
        return self.wall_list


"""
This class needs a get_walls method to return the walls of the room in the form of a list.
"""




