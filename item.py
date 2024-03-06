
"""
Quick comments from Skyler:
I think that we will actually want to be loading the items from a json, somewhat like rooms.
- So, each item in the json will have weight and sprite png (so you can use arcades sprite from png to make the actual sprite)

For value ranges, if a 0 is passed in, the value is 10-30, 1 is 30-60 and 2 is 60-100 (just use this to set the value of this sprite)
I would split up the json into two areas, being one handed and two handed, and then value range 
(i.e. "0" for 0 value items, see resources/items.json for this)
- for instance, if a 0 is passed in for value, and it isn't a two-handed item:
        assign self.value of randint(10, 30), and randomly choose something from
        Load the json (using json.load) and access the list of items of value 0 using following:
        data_from_json["one_handed"]["0"]     Then randomly pull from this for the weight and specific sprite

"""

import arcade
import json
import random


class Item(arcade.Sprite):
    def __init__(self):
        """
        initialize value, size, type, is_two_handed
        """
        super().__init__()
        self.weight = None
        self.value = None
        self.texture = None
        self.texture_inventory = None
        self.texture_map = None
        self.type = None
        self.two_handed = None

    def setup(self, x_center, y_center, value, is_two_handed):
        """
        Update the variables based on these
        :param x_center:
        :param y_center:
        :param value:
        :param is_two_handed:
        """
        self.center_x = x_center
        self.center_y = y_center

        # Determine value range
        if value == 0:
            value_range = "0"
        elif value == 1:
            value_range = "1"
        else:
            value_range = "2"

        # Determine if one-handed or two-handed
        item_type = "one_handed" if not is_two_handed else "two_handed"

        # Load item data from JSON
        with open("resources/items.json", "r") as file:
            data_from_json = json.load(file)

        # Choose random item from the specified range and type
        items = data_from_json[item_type][value_range]
        item = random.choice(items)

        # Generate random value within the specified range
        value_lower, value_upper = item["value_range"]
        self.value = random.randint(value_lower, value_upper)

        # Assign weight and texture (for each of the two textures)
        self.weight = item["weight"]
        self.texture_map = item["sprite_filename"]
        self.texture = arcade.load_texture(item["sprite_filename"])
        self.texture_inventory = item["sprite_inventory_filename"]
        self.two_handed = is_two_handed

        return self

    def set_inventory_texture(self):
        """
        Switch self.texture from map texture to inventory texture
        """
        self.texture = arcade.load_texture(self.texture_inventory)

    def set_map_texture(self):
        """
        switch self.texture from inventory to map
        """
        self.texture = arcade.load_texture(self.texture_map)
