import arcade


class Item(arcade.Sprite):
    def __init__(self):
        """
        initialize value, size, type, is_two_handed
        """
        super().__init__()

    def setup(self, type, size, value, is_two_handed):
        """
        Update the variables based on these
        :param type:
        :param size:
        :param value:
        :return:
        """


