import arcade


class Item(arcade.Sprite):
    def __init__(self):
        """
        initialize value, size, type, is_two_handed
        """
        super().__init__()
        self.weight = None
        self.value = None
        self.texture = None
        self.type = None
        self.two_handed = None

    def setup(self, x_center, y_center, type, size, value, is_two_handed):
        """
        Update the variables based on these
        :param type:
        :param size:
        :param value:
        :return:
        """



