import arcade


class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        """
        populate this with inventory items, holding_two handed boolean,
        current_item_slot_selected,

        """

        """
        current item slot selected:
        when a player tries to pick up something, don't allow them to do this if they're holding something
        This will likely be done in the game class (as most things are), but we need to block the player from 
        picking something up if the current item slot 
        """


