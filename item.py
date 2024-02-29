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
        I think that we will actually want to be loading the items from a json, somewhat like rooms.
        - So, each item in the json will have weight and sprite png (so you can use arcades sprite from png to make the actual sprite)
        
        For value ranges, if a 0 is passed in, the value is 10-30, 1 is 30-60 and 2 is 60-100 (just use this to set the value of this sprite)
        I would split up the json into two areas, being one handed and two handed, and then value range 
        (i.e. "0" for 0 value items, see resources/items.json for this)
        - for instance, if a 0 is passed in for value, and it isn't a two-handed item:
                assign self.value of randint(10, 30), and randomly choose something from
                Load the json (using json.load) and access the list of items of value 0 using following:
                data_from_json["one_handed"]["0"]     Then randomly pull from this for the weight and specific sprite

        Feel free to use my stuff in Room setup as an example for how to use the json with this. 
        

        """



