import arcade


class room(arcade.Sprite):
    def __init__(self):
        """
        Spawn areas (coordinates for bounding boxes, list of list of tuples), room type,
        doors, loot_item_spawn_list
        """

    def setup(self, room_type, item, x_top_left, y_top_left):
        """
        loot_value
        :return:
        """