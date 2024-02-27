import arcade


class Map(arcade.Sprite):
    def __init__(self):
        """
        This needs to have an overall wall list, created when making all the rooms together.
        the Room class needs to implement a Room.get_walls method for this
        """

    def setup(self):
        """
        Generating
        :return:
        """
        map = generate_map()
        room.setup(map[i][j], x_top_left, y_top_left)

def generate_map():
    """
    Generate the array representation of the map
    :return:
    """



