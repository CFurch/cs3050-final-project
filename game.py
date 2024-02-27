"""
CS 3050 Team 5


"""

import arcade
from room import Room
from map import Map, generate_map
from player import PlayerCharacter
from item import Item

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "2D Lethal Company"

# Starting location of the player, and movement constants
PLAYER_START_X = 2
PLAYER_START_Y = 1
MAX_STAM = 100
STAM_DRAIN = 2 # Stam drain 2, will be divided by 2 for stamina increase rate
BASE_MOVEMENT_SPEED = 5


class LethalGame(arcade.Window):
    """
    Main class for running the game
    """

    def __init__(self):
        """
        Initializer
        """
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Initialize variables for spawning / map / other important variables
        self.map = None
        self.walls = None
        self.player = None
        self.enemy_entities = None
        self.loot_items = None
        self.physics_engine = None

        # GUI variables
        self.camera = None
        self.scene = None

        # Movement / inventory variables
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.shift_pressed = False
        self.pressed_1 = False
        self.pressed_2 = False
        self.pressed_3 = False
        self.pressed_4 = False
        self.e_pressed = False
        self.g_pressed = False

        self.movement_speed = BASE_MOVEMENT_SPEED # speed is pixels per frame
        self.sprinting = False

        # Inventory slots
        self.current_inv_slot = 1 # Start in first inventory slot
        self.try_pickup_item = False
        self.drop_item = False

        # Set power levels - has to do with spawning mechanics
        self.indoor_power = 4  # experimentation-40 levels

    def setup(self, procgen_results):
        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Set up the map, using procgen and the map class (passed in as parameters
        # Ideally this would work using some sort of arcade.load_tilemap(map_name)
        # if we use this we need to use layers for the physics engine, otherwise add
        # all walls to the walls list
        self.map = Map()
        self.map.setup()
        # get the walls from the map
        # self.walls = self.map.get_walls()

        # self.scene = arcade.Scene.from_tilemap(self.map)

        # Initialize player character
        self.player = PlayerCharacter()
        # Add logic for starting location of player
        self.player.center_x = PLAYER_START_X
        self.player.center_y = PLAYER_START_Y

        # Add player to the scene
        self.scene.add_sprite(self.player)

        # Add enemies to scene - spawner class needs to handle these
        # for enemy in self.enemy_entities:
        #     self.scene.add_sprite(enemy)

        # Add loot items to scene
        # for item in loot_items:
        #     self.item_list.append(item)
        #     self.scene.add_sprite(item)

        # Set background color to be black
        arcade.set_background_color(arcade.color.BLACK)

        # Create physics engine - we can use the platformer without gravity to get the intended effect
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, walls=self.walls
        )

    def on_draw(self):
        """
        Render the screen
        """
        # Clear the screen
        self.clear()

        # Draw the scene
        self.scene.draw()

        # Draw the health and stamina into upper left
        health_text = f"Health: {self.player.get_health()}"
        stamina_text = f"Stamina: {self.player.get_stam()}"
        arcade.draw_text(health_text, 10, 10, arcade.csscolor.RED, 18)
        arcade.draw_text(stamina_text, 10, 20, arcade.csscolor.ORANGE, 18)

    def process_keychange(self):
        """
        This function is used for changing the state of the player
        """
        # Update movement speed if shift is pressed - if sprinting, base movement speed should be doubled
        # Check on the current movement speed to ensure this
        if self.player.get_stam > 0 and self.shift_pressed and self.movement_speed != BASE_MOVEMENT_SPEED * 2:
            # nice to have: account for horizontal movement speed
            self.movement_speed = BASE_MOVEMENT_SPEED * 2
            self.sprinting = True # Use sprinting variable to signal to update that sprint
            # is happening and decrement player's sprint
        elif not self.shift_pressed and self.movement_speed != BASE_MOVEMENT_SPEED:
            self.movement_speed = BASE_MOVEMENT_SPEED
            self.sprinting = False

        # Process up/down
        if self.up_pressed and not self.down_pressed:
            self.player.change_y = self.movement_speed
        elif self.down_pressed and not self.up_pressed:
            self.player.change_y = -self.movement_speed
        else:
            self.player.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player.change_x = self.movement_speed
        elif self.left_pressed and not self.right_pressed:
            self.player.change_x = -self.movement_speed
        else:
            self.player.change_x = 0

        # determine the current inventory slot to pull from
        if self.pressed_1:
            self.current_inv_slot = 1
        elif self.pressed_2:
            self.current_inv_slot = 2
        elif self.pressed_3:
            self.current_inv_slot = 3
        elif self.pressed_4:
            self.current_inv_slot = 4

        # Handling if attempting to pick something up
        if self.e_pressed:
            self.try_pickup_item = True
        else:
            self.try_pickup_item = False

        # Handling if trying to drop something
        if self.g_pressed:
            self.drop_item = True
        else:
            self.drop_item = False

    def on_key_press(self, key, modifiers):
        """
        Handling key presses
        :param key: the key object to be pressed
        :param modifiers:
        """
        # In some examples, these are in if elif blocks, this is changed to if statements
        # to allow multiple directions to be pressed at once (only to allow up/down or right/left)
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        # Handle attempt_sprint
        if key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
            self.shift_pressed = True

        # for picking up and dropping items
        if key == arcade.key.E:
            self.e_pressed = True
        elif key == arcade.key.G:
            self.g_pressed = True

        # for changing selected inventory slots
        if key == arcade.key.KEY_1:
            self.pressed_1 = True
        elif key == arcade.key.KEY_2:
            self.pressed_2 = True
        elif key == arcade.key.KEY_3:
            self.pressed_3 = True
        elif key == arcade.key.KEY_4:
            self.pressed_4 = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """
        Handling the releases of keys
        :param key:
        :param modifiers:
        """
        # Deselect key presses
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        if key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
            self.shift_pressed = False

        if key == arcade.key.E:
            self.e_pressed = False
        elif key == arcade.key.G:
            self.g_pressed = False

        if key == arcade.key.KEY_1:
            self.pressed_1 = False
        elif key == arcade.key.KEY_2:
            self.pressed_2 = False
        elif key == arcade.key.KEY_3:
            self.pressed_3 = False
        elif key == arcade.key.KEY_4:
            self.pressed_4 = False

        self.process_keychange()

    def center_camera_to_player(self):
        """
        Needed for centering the camera to the player on each game tick
        """
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered, 0.2)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # Update player speed based on stamina
        if self.sprinting:
            self.player.decrease_stam(STAM_DRAIN)
        elif self.player.get_stam() < MAX_STAM:
            self.player.increase_stam(STAM_DRAIN / 2)

        # Update Animations
        # self.scene.update_animation(
        #     delta_time,
        #     [
        #         LAYER_NAME_COINS,
        #         LAYER_NAME_BACKGROUND,
        #         LAYER_NAME_PLAYER,
        #         LAYER_NAME_ENEMIES,
        #     ],
        # )

        # Update walls, used with moving platforms
        self.scene.update(self.walls)

        # handle collisions - like this
        # item_hit_list = arcade.check_for_collision_with_list(
        #     self.player_sprite, self.scene[LAYER_NAME_ITEMS] # may need to change layer name
        # )
        # Handle checking if items are in hitbox and the player is attempting to pick something up
        # Add the item to inventory if the player's current slot is open
        # if self.try_pickup_item and not self.player.get_inv(self.current_inv_slot):
        #     # Since we can only populate the player's inventory slot with a single item,
        #     # we will only try with the first item
        #     item_hit_list = arcade.check_for_collision_with_list(self.player, self.loot_items)
        #     if len(item_hit_list) > 0:
        #         self.player.add_item(self.current_inv_slot, item_hit_list[0])
        #         self.loot_items.remove(item_hit_list[0]) # I'm not too sure how well this will work, have to try later
        #         item_hit_list[0].remove_from_sprite_lists() # remove from sprite list too
        #
        # # Handle checking if the player wants to drop items
        # if self.drop_item and self.player.get_inv(self.current_inv_slot):
        #     temp_item = self.player.remove_item(self.current_inv_slot)
        #     # Currently I will be including all of this, I'm not sure if we need to have both
        #     self.scene.add_sprite(temp_item)
        #     self.loot_items.append(temp_item)

        # Position the camera
        self.center_camera_to_player()


def main():
    """
    Main function
    """
    # Generate the map representation
    procgen_output = generate_map()

    # Initialize game and begin runtime
    window = LethalGame()
    window.setup(procgen_output)
    arcade.run()


if __name__ == "__main__":
    main()

"""
Framework for game

from game startup:
- player chooses level (skip at start)
- procgen is called with map data (determines an array representation of the indoor map)
- map setup is called with procgens results as an argument
  - puts tile spaces together, creates room class objects (by passing spawn items)
- all these are done within game setup
-
- player entity is rendered


"""
