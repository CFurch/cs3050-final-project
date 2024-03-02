import arcade


class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        """
        populate this with inventory items, holding_two handed boolean,
        current_item_slot_selected, health, and stamina

        """
        super().__init__()

        # Inventory attributes
        self.inventory = [None, None, None, None]  # Assuming 4 inventory slots
        self.holding_two_handed = False
        self.current_item_slot_selected = 1  # Default to first slot
        self.health = 100
        self.stamina = 100
        self.movement_speed = None
        # Need to update sprites with animations, directions, etc
        self.texture = arcade.load_texture("resources/player_sprites/player_sprite_temp.png")

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

    # get_health() - returns health value
    def get_health(self):
        return self.health

    # get_stam() - returns stamina value
    def get_stam(self):
        return self.stamina

    """
    get_inv(int) - returns the boolean value of the inputted inventory slot (true if something in it, false if not)
    - return false if player is holding a two-handed item (holding_two_handed is true), even if the other slot is full
    - this will be 1 indexed: first inventory slot is 1, second is 2, etc
    """

    def get_inv(self, inventory_slot):
        # Check if holding a two-handed item
        if self.holding_two_handed:
            return False
        # Adjust for 1-indexed slots
        slot_index = inventory_slot - 1
        return self.inventory[slot_index] is not None

    # set_two_handed(bool) set two handed
    def set_two_handed(self, is_two_handed):
        self.holding_two_handed = is_two_handed

    """
    add_item(inventory_slot, item)
    - you don't need to handle for the inventory slot being open or closed
    - item will be an instance of the Item class, simply update the index of inventory_slot - 1 with this item
    """

    def add_item(self, inventory_slot, item):
        # Adjust for 1-indexed slots
        slot_index = inventory_slot - 1
        self.inventory[slot_index] = item

    """
    remove_item(inventory_slot)
    - remove and return the object of the index of inventor_slot - 1, then set that index to be None (or whatever the 
      default empty value you decide for it) (the x and y coordinates of the item object need to be updated to the player's current location
      (This should be some sort of call to self.center_x and self.center_y to access the player Sprite's center
      """

    def remove_item(self, inventory_slot):
        # Adjust for 1-indexed slots
        slot_index = inventory_slot - 1
        removed_item = self.inventory[slot_index]
        self.inventory[slot_index] = None
        # Update items coordinates to the player's coordinates
        removed_item.center_x = self.center_x
        removed_item.center_y = self.center_y
        return removed_item

    def decrease_stam(self, amount):
        self.stamina -= amount
        if self.stamina < 0:
            self.stamina = 0

    def decrease_health(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def add_stam(self, amount):
        self.stamina += amount
        if self.stamina > 100:  # Assuming max stamina is 100
            self.stamina = 100

    def add_health(self, amount):
        self.health += amount
        if self.health > 100:  # Assuming max health is 100
            self.health = 100

    def set_current_inv_slot(self, inventory_slot):
        """
        Set the currently selected inventory slot, unless there is a two-handed object being held.
        """
        if not self.holding_two_handed:
            self.current_item_slot_selected = inventory_slot

    def get_current_inv_slot(self):
        """
        Getter for the currently selected inventory slot.
        """
        return self.current_item_slot_selected

    def set_movement_speed(self, speed):
        self.movement_speed = speed

    def get_movement_speed(self):
        return self.movement_speed

    """
    future todo:
    Add self.current_texture variable, set to 0. In init, load each texture (into self.walk_textures) 
    for how many are in the animation and then use this loop in update_animation to change the player sprite
    self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture]
    additionally implement facing direction to this (although this will likely be rotating the sprite
    """
