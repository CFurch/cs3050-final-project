import arcade
import random
import json
from player import PlayerCharacter
from item import Item
import keyboard


MAX_DOOR_BATTERY = 100
DOOR_BATTERY_DRAIN = 0.2
DOOR_SPRITE_X = 64 + 16
DOOR_SPRITE_Y = 248 + 16
SHIP_LAYER_NAMES = ["walls", "background", "door_control", "lever", "terminal"]
DELAY_INTERACTIONS = 5
DELAY_DRAIN = 0.1
GAMESTATE_OPTIONS = {"orbit": 0, "outdoors": 1, "indoors": 2, "company": 3}
SHIP_INTERACTION_OPTIONS = {"lever": 0, "door": 1, "terminal": 2}
SCREEN_HEIGHT = 650


class Ship(arcade.Sprite):
    def __init__(self):
        """
        intialize the walls, background, textures
        To note, we will not be supporting moving things around the ship.
        """
        super().__init__()
        self.tilemap = None # Will also function as the walls of the ship

        # Interaction areas are handled in the tilemap

        self.in_orbit = True # Ship starts in orbit

        # Door movement (starts shut with no battery drain)
        self.door_closed = True
        self.door_sprite = None
        self.door_battery = MAX_DOOR_BATTERY
        self.door_battery_drain = 0
        self.interact_delay = 0
        # Need delay starting at max
        self.lever_delay = DELAY_INTERACTIONS

        self.ship_loot = None
        self.total_loot_value = 0

        # For terminal interaction
        self.player_interacting_with_terminal = False
        self.terminal_input = ""
        self.terminal_output = ""
        self.processed_output = ""
        self.short_output = ""
        self.money = 0

    def setup(self):
        # Load tilemap
        self.tilemap = arcade.Scene.from_tilemap(arcade.load_tilemap("resources/tilemaps/ship.tmx"))
        # The door sprite
        self.door_sprite = arcade.Sprite("resources/wall_sprites/closed_door.png")
        self.door_sprite.center_x += DOOR_SPRITE_X
        self.door_sprite.center_y += DOOR_SPRITE_Y
        # The loot present on the ship
        self.ship_loot = arcade.SpriteList()

        return self

    def update_position(self, delta_x, delta_y):
        # Update the position of the ship sprite
        self.center_x += delta_x
        self.center_y += delta_y

        # Update the position of each sprite within the tilemap
        for layer_name in SHIP_LAYER_NAMES:
            layer = self.tilemap[layer_name]
            for sprite in layer:
                sprite.center_x += delta_x
                sprite.center_y += delta_y

        self.door_sprite.center_x += delta_x
        self.door_sprite.center_y += delta_y

        for item in self.ship_loot:
            item.center_x += delta_x
            item.center_y += delta_y

    def get_pos(self):
        return self.center_x, self.center_y

    def draw_self(self, camera, gamestate):
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

        # Draw ship loot
        for item in self.ship_loot:
            item.draw_self()

        # Draw the amount of loot onto the hud if in orbit
        if gamestate == GAMESTATE_OPTIONS["orbit"] and not self.player_interacting_with_terminal:
            text_x = camera.position[0] + 20
            text_y = camera.position[1] + SCREEN_HEIGHT - 30
            arcade.draw_text(f"Total ship loot: {self.total_loot_value}", text_x, text_y - 210, arcade.csscolor.GREEN, 18)

    def add_item(self, item):
        self.ship_loot.append(item)
        self.total_loot_value += item.get_value()

    def remove_item(self, item):
        self.ship_loot.remove(item)
        self.total_loot_value -= item.get_value()
        if self.total_loot_value < 0:
            self.total_loot_value = 0

    def get_walls(self):
        # Create a SpriteList containing the walls
        wall_list = arcade.SpriteList()
        wall_list.extend(self.tilemap["walls"])

        # Append the door sprite when it is closed
        if self.door_closed:
            wall_list.append(self.door_sprite)

        return wall_list

    def get_background_hitbox(self):
        return self.tilemap["background"]

    def interact_ship(self, player):
        """
        This function has to do with interaction between the player and things on the ship.
        Having the delays in here makes it so that player interaction using the "e" key
        makes delays only happen when the player is interacting. In practice this is honestly fine.
        :param player: PlayerCharacter object
        :param camera: Camera object to draw onto hud
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
                return SHIP_INTERACTION_OPTIONS["door"]
            self.interact_delay -= DELAY_DRAIN
        elif arcade.check_for_collision_with_list(player, self.tilemap["lever"]):
            if self.lever_delay <= 0:
                # Lever is activated
                self.lever_delay = DELAY_INTERACTIONS
                return SHIP_INTERACTION_OPTIONS["lever"]
            self.lever_delay -= DELAY_DRAIN
        elif arcade.check_for_collision_with_list(player, self.tilemap["terminal"]):
            if self.interact_delay <= 0:
                # Set the player to be interacting with the terminal
                self.interact_delay = DELAY_INTERACTIONS
                # print("getting input")
                # Interact with keyboard / listen for input
                self.player_interacting_with_terminal = True

                return SHIP_INTERACTION_OPTIONS["terminal"]
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
            self.door_closed = False
        else:
            self.in_orbit = True
            self.door_battery_drain = 0
            self.door_closed = True

    def interact_terminal(self):
        """
        This will handle terminal interaction, which will require a different UI than normal. However, this can be drawn
        over the rest of the screen with some opacity. (like in game)
        This handles inputs from user for things like the moons, etc. This functions as a very simple parser
        :return:
        """
        return ""

    def get_door(self):
        return self.door_closed

    def get_loot(self):
        return self.ship_loot

    def set_loot(self, spritelist):
        self.ship_loot = spritelist

    def add_terminal_input(self, key):
        """
        Adds a single keypress to the input string
        """
        if key == arcade.key.ENTER:
            # Save terminal input into output(checked by process)
            self.terminal_output = self.terminal_input
            self.terminal_input = ""  # Reset input string after printing
        elif key == arcade.key.BACKSPACE:
            self.terminal_input = self.terminal_input[:-1]  # Remove last character
        elif key == arcade.key.ESCAPE:
            self.player_interacting_with_terminal = False
            self.processed_output = ""
            self.terminal_output = ""
            self.terminal_input = ""
            # Add input into output variable and reset input
        elif key in (arcade.key.LSHIFT, arcade.key.RSHIFT, arcade.key.NUMLOCK, arcade.key.CAPSLOCK,
                     arcade.key.LCTRL, arcade.key.RCTRL, arcade.key.LALT, arcade.key.RALT,
                     arcade.key.LMETA, arcade.key.RMETA):
            pass  # Ignore special keys
        else:
            # Add pressed character to input string
            self.terminal_input += chr(key)

    def check_terminal_input(self, gamestate):
        """
        Checks to see if there is any terminal output
        """
        if self.terminal_output != "":
            # output to user and reset terminal outpute
            self.short_output, self.processed_output = process_input(self.terminal_output, gamestate)
            self.terminal_output = ""

    def read_output(self):
        return self.short_output, self.processed_output


def process_input(input_string, gamestate):
    """
    Processes string input, in basic form. Many of the inputs are hardcoded
    :param input_string: String
    """
    input_string = input_string.lower()
    # For routing to company building
    if input_string.startswith("com"):
        # print("company")
        return "comp", "Routing to company building"
    elif input_string.startswith("moo"):
        # Load moon names
        rtn_string = "Available moons: "
        with open('resources/moons.json', 'r') as f:
            data = json.load(f)
        for moon in data:
            rtn_string += "\n" + moon["moon_name"]
        return "moons", rtn_string
    elif input_string.startswith("help"):
        return "help", "moons: shows list of available moons\n\n" \
                       "company building: route to company building\n\n" \
                       "store: shows store items for purchase\n\n" \
                       "Exit terminal using escape key"
    elif input_string.startswith("sto"):
        return "store", "Store"
    else:
        # Only allow moon switching while in orbit
        if gamestate == GAMESTATE_OPTIONS["orbit"]:
            # Load moon data for terminal phrases - done after other inputs to not load every time
            with open('resources/moons.json', 'r') as f:
                data = json.load(f)
            # check if terminal phrase starts with a moon phrase
            for obj in data:
                if input_string.startswith(obj['terminal_phrase']):
                    return obj['terminal_phrase'], f"Routing to {obj['moon_name']}"
        else:
            return "", "Cannot change moon unless in orbit"
        return None, "Invalid input"



