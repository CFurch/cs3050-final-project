import json
import random

import arcade

from item import Item



class Room(arcade.Sprite):
    def __init__(self):
        """
        Spawn areas (coordinates for bounding boxes (x, y), list of list of tuples), room type,
        doors, loot_item_spawn_list, wall_list
        """
        super().__init__()
        self.wall_list = None
        self.loot_item_spawn_list = None
        self.loot_list = None # This list will be populated with loo class objects based off the above list
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
        self.loot_list = arcade.SpriteList()
        self.loot_item_spawn_list = loot_item_spawn_list
        self.spawners = arcade.SpriteList() # spawners will be an arcade sprite list, the value passed into spawners is int of how many to have
        self.hazards = hazards
        self.room_type = room_type
        self.x_center = x_center
        self.y_center = y_center

        # Load room data from JSON file
        with open("resources/rooms.json") as f:
            rooms_data = json.load(f)

        # Pull the specific rooms data from the json based on room type bitwise representation
        rooms_data = rooms_data["rooms"].get(room_type, {})
        # Get walls data
        walls_data = rooms_data.get("walls", [])

        # Create walls based on walls data
        for wall_data in walls_data:
            center_x = wall_data["center_x"] + self.x_center
            center_y = wall_data["center_y"] + self.y_center
            width = wall_data["width"]
            height = wall_data["height"]
            self.create_wall(center_x, center_y, width, height)

        # Spawn loot
        # Get spawn location(s) of room
        item_spawn_areas = rooms_data.get("item_spawn_areas", [])
        # Handle spawning item
        is_two_handed = False
        for temp_list in self.loot_item_spawn_list:
            item_value = 0
            for temp_item in temp_list:
                if temp_item != 0:
                    # spawn that many items that are being asked for
                    for i in range(temp_item):
                        # Choose a random loot spawn area
                        spawn_area = random.randint(0, len(item_spawn_areas) - 1)
                        # select a point in the spawn area - use of integer division to ensure integer bounds
                        random_x_val = random.randint(self.center_x + item_spawn_areas[spawn_area]["center_x"] -
                                                      item_spawn_areas[spawn_area]["width"] // 2, self.center_x +
                                                      item_spawn_areas[spawn_area]["center_x"] + item_spawn_areas[spawn_area]["width"] // 2)
                        random_y_val = random.randint(self.center_y + item_spawn_areas[spawn_area]["center_y"] -
                                                      item_spawn_areas[spawn_area]["height"] // 2, self.center_x +
                                                      item_spawn_areas[spawn_area]["center_y"] + item_spawn_areas[spawn_area][
                                                          "height"] // 2)
                        # Create a loot item
                        loot_item = Item().setup(random_x_val, random_y_val, item_value, is_two_handed)

                        # Add the loot item to the room's item list
                        self.loot_list.append(loot_item)

                item_value += 1

            is_two_handed = True

        # We may need to add information to spawner class to actually indicate where the monsters will spawn out of a
        # vent. This could be done using a unit vector representation of a direction, and continuously attempt to spawn
        # a monster until it isn't clipping a wall with its hitbox
        # Create spawners (later)
        # spawn_locations = rooms_data.get("spawner_locations", [])
        # attempts_made = 0
        # while len(spawn_locations) > 0:
        #     # ensure there are still valid spawn locations
        #     if attempts_made > len(spawn_locations) or len(spawn_locations) == 0:
        #         break
        #     # Create spawner object, use and remove a random spawn location
        #     random_index = random.randint(0, len(spawn_locations) - 1)
        #     location_dict = spawn_locations.pop(random_index)
        #     # call spawner creator with self.x_center + location_dict["x"] and similarly for y to make a spawner
        #     # additionally with other methods for determining spawner positioning (spawn direction)

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
        wall = arcade.SpriteSolidColor(width, height, arcade.csscolor.GRAY) # change this depending on what we want
        # Will likely have to change how the walls are stored to instead store file locations to sprite pngs
        wall.center_x = center_x
        wall.center_y = center_y
        self.wall_list.append(wall)

    def get_walls(self):
        return self.wall_list

"""
This class needs a get_walls method to return the walls of the room in the form of a list.
"""

"""
TO DO: Getters and Setters for all values
"""



