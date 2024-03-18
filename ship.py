import arcade
import random
import json
from player import PlayerCharacter

MAX_DOOR_BATTERY = 100
DOOR_BATTERY_DRAIN = 0.2
DOOR_SPRITE_X = 64
DOOR_SPRITE_Y = 248
SHIP_LAYER_NAMES = ["walls", "background", "door_control", "lever", "terminal"]
DELAY_INTERACTIONS = 5
DELAY_DRAIN = 0.1


class Ship(arcade.Sprite):
    def __init__(self):
        """
        intialize the walls, background, textures
        To note, we will not be supporting moving things around the ship.
        """
        super().__init__()
        self.tilemap = None # Will also function as the walls of the ship

        # Interaction areas are handled in the tilemap

        self.in_orbit = False

        # Door movement
        self.door_closed = False
        self.door_sprite = None
        self.door_battery = MAX_DOOR_BATTERY
        self.door_battery_drain = DOOR_BATTERY_DRAIN
        self.interact_delay = 0
        # Need delay starting at max
        self.lever_delay = DELAY_INTERACTIONS

    def setup(self):
        # Load tilemap
        self.tilemap = arcade.Scene.from_tilemap(arcade.load_tilemap("resources/tilemaps/ship.tmx"))
        self.door_sprite = arcade.Sprite("resources/wall_sprites/closed_door.png")

        return self

    def update_position(self, x, y):
        # Update the position of the ship sprite
        self.center_x = x
        self.center_y = y

        # Update the position of each sprite within the tilemap
        for layer_name in SHIP_LAYER_NAMES:
            layer = self.tilemap[layer_name]
            for sprite in layer:
                sprite.center_x += x
                sprite.center_y += y

        self.door_sprite.center_x = x + DOOR_SPRITE_X
        self.door_sprite.center_y = y + DOOR_SPRITE_Y

    def draw_self(self):
        # Only draw the layers we want to have drawn - bounding boxes and interaction boxes aren't needed
        self.tilemap["background"].draw()
        self.tilemap["walls"].draw()
        # These will be removed later but here for debugging temporarily
        self.tilemap["door_control"].draw()
        self.tilemap["lever"].draw()
        self.tilemap["terminal"].draw()
        # Draw the door if it is closed
        if self.door_closed:
            self.door_sprite.draw()

    def get_walls(self):
        # Create a SpriteList containing the walls
        wall_list = arcade.SpriteList()
        wall_list.extend(self.tilemap["walls"])

        # Append the door sprite when it is closed
        if self.door_closed:
            wall_list.append(self.door_sprite)

        return wall_list

    def interact_ship(self, player):
        """
        This function has to do with interaction between the player and things on the ship
        :param player: PlayerCharacter object
        :return: String, result of interaction
        """

        if arcade.check_for_collision_with_list(player, self.tilemap["door_control"]):
            if self.interact_delay <= 0:
                self.interact_delay = DELAY_INTERACTIONS
                # print("door controls manip")
                # reverse door state, if not in orbit
                if not self.in_orbit:
                    self.door_closed = not self.door_closed
                else:
                    self.door_closed = True
                return "door"
            self.interact_delay -= DELAY_DRAIN
        elif arcade.check_for_collision_with_list(player, self.tilemap["lever"]):
            if self.lever_delay <= 0:
                self.lever_delay = DELAY_INTERACTIONS
                # possibly call self.change_orbit
                # print("lever manip")
                return "lever"
            self.lever_delay -= DELAY_DRAIN
        elif arcade.check_for_collision_with_list(player, self.tilemap["terminal"]):
            if self.interact_delay <= 0:
                self.interact_delay = DELAY_INTERACTIONS
                # print("terminal manip")
                return "terminal"
            self.interact_delay -= DELAY_DRAIN

    def update_ship(self):
        # Logic for decreasing battery while door is closed and increasing when open
        if self.door_closed and self.door_battery > 0:
            self.door_battery -= DOOR_BATTERY_DRAIN
            if self.door_battery <= 0:
                self.door_closed = False
        elif not self.door_closed and self.door_battery < 100:
            self.door_battery += DOOR_BATTERY_DRAIN * 3 # door battery recovers faster

    def change_orbit(self):
        """
        Door battery drain needs to be zero when in orbit
        :return:
        """
        if self.in_orbit:
            self.in_orbit = False
            self.door_battery_drain = DOOR_BATTERY_DRAIN
        else:
            self.in_orbit = True
            self.door_battery_drain = 0

    def get_door(self):
        return self.door_closed
