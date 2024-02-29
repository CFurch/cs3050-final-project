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

    def setup(self, x_center, y_center, weight, value, is_two_handed): # Add type to this if need, skyler doesn't remember what that was for
        """
        Update the variables based on these
        :param type:
        :param size:
        :param value:
        :return:
        """


"""
Quick comments from Skyler:
I think that we will actually want to be loading the items from a json, like rooms.
So, each item in the json will have weight and sprite png
For value ranges, if a 0 is passed in, the value is 10-30, 1 is 30-60 and 2 is 30-100
I would split up the json into two areas, being one handed and two handed, and then value range 
(i.e. "0" for 0 value items, see the json for this)
I'll make an example json of this, to show what I'm thinking. Feel free to use my stuff in Room setup
as an example for how to use it


"""
