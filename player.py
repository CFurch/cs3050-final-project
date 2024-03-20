import arcade
import math

PLAYER_DELAY_PICKUP_DROP = 20
PLAYER_ROTATION_RATE = 10


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
        self.total_weight = 0
        # Need to update sprites with animations, directions, etc
        self.texture = arcade.load_texture("resources/player_sprites/player_neutral.png")
        self.rotation = 0

        # Block pickup if player is just dropped something or just picked something up
        self.pickup_drop_delay = 0

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
        # Adjust for 1-indexed slots
        slot_index = inventory_slot - 1
        return self.inventory[slot_index] is not None

    def get_full_inv(self):
        return self.inventory

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
        item.set_inventory_texture()
        self.inventory[slot_index] = item
        self.holding_two_handed = item.two_handed
        self.total_weight += item.weight

        # reset item drop/pickup delay
        self.reset_pd_delay()

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
        # Set holding_two_handed to be false if item was two handed
        if removed_item.two_handed:
            self.holding_two_handed = False
        self.total_weight -= removed_item.weight
        # Update items coordinates to the player's coordinates, and update items texture
        removed_item.set_map_texture()
        removed_item.center_x = self.center_x
        removed_item.center_y = self.center_y

        # reset pickup drop delay
        self.reset_pd_delay()

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

    def get_two_handed(self):
        return self.holding_two_handed

    def get_weight(self):
        return self.total_weight

    def get_pd_delay(self):
        return self.pickup_drop_delay

    def decrease_pd_delay(self):
        if self.pickup_drop_delay > 0:
            self.pickup_drop_delay -= 1

    def reset_pd_delay(self):
        self.pickup_drop_delay = PLAYER_DELAY_PICKUP_DROP

    def update_rotation(self, x_direction, y_direction):
        """
        This is done by calculating the target direction for the player to turn, and then updating the players
        current direction by a step
        :param x_direction:
        :param y_direction:
        :return:
        """
        # Calculate target direction using arctan
        target_direction = math.degrees(math.atan2(y_direction, x_direction))

        # Normalize target direction to be in the range [0, 360) (arctan is in range -180 to 180)
        target_direction = (target_direction + 360) % 360
        current_rotation = self.rotation % 360

        # Calculate the absolute difference between target direction and current rotation
        diff_clockwise = (target_direction - current_rotation) % 360
        diff_counterclockwise = (current_rotation - target_direction) % 360

        # Determine the direction (clockwise or counterclockwise) to rotate
        if diff_clockwise <= diff_counterclockwise:
            rotation_direction = 1  # Rotate clockwise
        else:
            rotation_direction = -1  # Rotate counterclockwise

        # Adjust rotation rate if rotation is close to target (reduce stuttering
        if min(diff_clockwise, diff_counterclockwise) < PLAYER_ROTATION_RATE:
            rotation_rate = PLAYER_ROTATION_RATE / 2
            # Decrease again if closer
            if min(diff_clockwise, diff_counterclockwise) < PLAYER_ROTATION_RATE / 2:
                rotation_rate = PLAYER_ROTATION_RATE / 4
        else:
            rotation_rate = PLAYER_ROTATION_RATE

        # Adjust rotation
        if current_rotation != target_direction:
            self.rotation += rotation_direction * rotation_rate

    def draw_self(self):

        """
        Draw the turret with scaled texture and rotation.
        """

        arcade.draw_texture_rectangle(self.center_x, self.center_y, self.texture.width * self.scale,
                                      self.texture.height * self.scale, self.texture, self.rotation)


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
