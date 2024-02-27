import arcade


class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        """
        populate this with inventory items, holding_two handed boolean,
        current_item_slot_selected, health, and stamina

        """

        """
        current item slot selected:
        when a player tries to pick up something, don't allow them to do this if they're holding something
        This will likely be done in the game class (as most things are), but we need to block the player from 
        picking something up if the current item slot 
        """

    def setup(self):
        """
        This may not be needed, add as wanted
        :return:
        """

"""
Needed functions:
get_health() - returns health value
get_stam() - returns stamina value

get_inv(int) - returns the boolean value of the inputted inventory slot (true if something in it, false if not)
- return false if player is holding a two-handed item (holding_two_handed is true), even if the other slot is full
- this will be 1 indexed: first inventory slot is 1, second is 2, etc

set_two_handed(bool) set two handed

add_item(inventory_slot, item)
- you don't need to handle for the inventory slot being open or closed
- item will be an instance of the Item class, simply update the index of inventory_slot - 1 with this item

remove_item(inventory_slot)
- remove and return the object of the index of inventor_slot - 1, then set that index to be None (or whatever the 
  default empty value you decide for it) (the x and y coordinates of the item object need to be updated to the player's current location
  (This should be some sort of call to self.center_x and self.center_y to access the player Sprite's center

decrease_stam(int), decrease_health(int)

get_stam(), get_health()

add_stam(), add_health()
(there are some health mechanics and cases for adding it)


"""
