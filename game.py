"""
CS 3050 Team 5


"""

import arcade
import math
from room import Room
from map import Map
from player import PlayerCharacter
from item import Item

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "2D Lethal Company"

# Starting location of the player, and movement constants
PLAYER_START_X = 500
PLAYER_START_Y = 500
MAX_STAM = 100
STAM_DRAIN = 0.17
BASE_MOVEMENT_SPEED = 2
SPRINT_DELAY = 30


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
        self.inventory_hud = None
        self.enemy_entities = None
        self.loot_items = None
        self.physics_engine = None

        # GUI variables
        self.camera = None
        # Instead of using a scene, it may also be easier to just keep a sprite list
        # for each individual thing.
        # self.scene = None

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

        self.sprinting = False
        self.delaying_stam = False

        # Inventory slots
        self.try_pickup_item = False
        self.drop_item = False

        # Set power levels - has to do with spawning mechanics
        self.indoor_power = None  # experimentation-40 levels

    def setup(self):
        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Set up the map, using procgen and the map class (passed in as parameters
        # Ideally this would work using some sort of arcade.load_tilemap(map_name)
        # if we use this we need to use layers for the physics engine, otherwise add
        # all walls to the walls list
        self.map = Map(0, 0)
        self.map.setup()
        # get the walls from the map
        self.walls = self.map.get_walls()
        self.loot_items = self.map.get_loot_list()
        # self.scene = arcade.Scene.from_tilemap(self.map)

        # Initialize player character
        self.player = PlayerCharacter()
        # Add logic for starting location of player
        self.player.center_x = PLAYER_START_X
        self.player.center_y = PLAYER_START_Y
        self.player.set_movement_speed(BASE_MOVEMENT_SPEED)  # speed is pixels per frame

        self.inventory_hud = arcade.SpriteList()
        # Add the four sprite items to the list
        for i in range(4):
            temp_sprite = arcade.Sprite("resources/item_sprites/inventory_box.png", scale=0.5)
            self.inventory_hud.append(temp_sprite)

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
        self.physics_engine.gravity_constant = 0

    def on_draw(self):
        """
        Render the screen
        """
        # Clear the screen
        self.clear()

        # Start the camera
        self.camera.use()

        # Draw the scene
        self.walls.draw()
        self.loot_items.draw()
        self.player.draw()

        # Draw the hud sprites
        temp_x = 300
        for slot in range(1, 5):
            if slot == self.player.get_current_inv_slot():
                sprite = arcade.Sprite("resources/item_sprites/inventory_box.png", scale=0.55)
            else:
                sprite = arcade.Sprite("resources/item_sprites/inventory_box_non_selected.png", scale=0.55)
            sprite.center_x = self.camera.position[0] + temp_x
            temp_x += 125
            sprite.center_y = self.camera.position[1] + 50
            sprite.alpha = 200
            sprite.draw()

        for idx, item in enumerate(self.player.get_full_inv()):
            if item != None:
                item.center_x = self.camera.position[0] + 300 + idx * 125
                item.center_y = self.camera.position[1] + 50
                # item.set_inventory_texture()
                # print(item.center_x, item.center_y)
                item.draw()

        # Draw text for holding 2 handed item
        if self.player.get_two_handed():
            holding_text = arcade.Sprite("resources/player_sprites/full_hands.png", scale=0.67)
            holding_text.center_x = self.camera.position[0] + SCREEN_WIDTH // 2 - 12
            holding_text.center_y = self.camera.position[1] + 50
            holding_text.draw()

        # Draw the health and stamina on the camera view
        # health_text = f"Health: {self.player.get_health()}"
        stamina_text = f"Stamina: {int(self.player.get_stam())}"
        weight_text = f"Weight: {int(self.player.get_weight())}"

        # Calculate the position for objects relative to the camera's position
        text_x = self.camera.position[0] + 20
        text_y = self.camera.position[1] + SCREEN_HEIGHT - 30

        # Draw the text at the calculated position
        # arcade.draw_text(health_text, text_x, text_y, arcade.csscolor.RED, 18)\
        health_sprite = arcade.Sprite(f"resources/player_sprites/player_health_sprite_{self.player.get_health() // 25}.png")
        health_sprite.center_x = self.camera.position[0] + 100
        health_sprite.center_y = self.camera.position[1] + SCREEN_HEIGHT - 100
        # health_sprite.alpha = 128 # use this to set opacity of objects
        health_sprite.draw()

        # Stamina representation
        arcade.draw_text(stamina_text, text_x, text_y - 180, arcade.csscolor.ORANGE, 18)
        arcade.draw_text(weight_text, text_x, text_y - 210, arcade.csscolor.ORANGE, 18)

    def process_keychange(self):
        """
        This function is used for changing the state of the player
        """
        # Update movement speed if shift is pressed - if sprinting, base movement speed should be doubled
        if not self.delaying_stam and self.shift_pressed and (self.up_pressed or self.down_pressed or self.right_pressed or self.left_pressed):
            self.sprinting = self.player.get_stam() > 0
        else:
            self.sprinting = False

        # Set movement speed
        if self.sprinting and not self.delaying_stam:
            self.player.set_movement_speed(BASE_MOVEMENT_SPEED * 2)  # Double speed when sprinting
        else:
            self.player.set_movement_speed(BASE_MOVEMENT_SPEED)

        # Delay stamina regeneration
        if self.delaying_stam:
            if self.player.get_stam() >= SPRINT_DELAY:
                self.delaying_stam = False
        # print(self.delaying_stam, self.sprinting)
        # Handle sprinting and stamina depletion
        if self.sprinting:
            if self.player.get_stam() < 1:
                self.delaying_stam = True
            else:
                # Decrease stamina based on players weight
                stam_drain_amount = STAM_DRAIN
                if self.player.get_weight() != 0:
                    stam_drain_amount *= 1 + 0.01 * self.player.get_weight()
                self.player.decrease_stam(stam_drain_amount)
        else:
            # Regenerate stamina if not sprinting
            if self.player.get_stam() < MAX_STAM:
                self.player.add_stam(STAM_DRAIN / 2)

        # Account for diagonal movement speed
        if self.up_pressed and self.right_pressed or self.down_pressed and self.right_pressed or \
                self.up_pressed and self.left_pressed or self.down_pressed and self.left_pressed:
            # Diagonal movement
            diagonal_speed = self.player.get_movement_speed() * (2 ** 0.5) / 2  # Movement speed for diagonal movement
            self.player.set_movement_speed(diagonal_speed)

        # Account for weight
        if self.player.get_weight() != 0:
            # reverse exponential function to decrease weight
            self.player.set_movement_speed(self.player.get_movement_speed() *
                                           math.exp(-0.01 * self.player.get_weight()))

        # print(self.player.get_movement_speed())
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            self.player.change_y = self.player.get_movement_speed()
        elif self.down_pressed and not self.up_pressed:
            self.player.change_y = -self.player.get_movement_speed()
        else:
            self.player.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player.change_x = self.player.get_movement_speed()
        elif self.left_pressed and not self.right_pressed:
            self.player.change_x = -self.player.get_movement_speed()
        else:
            self.player.change_x = 0

        # determine the current inventory slot to pull from
        if self.pressed_1:
            self.player.set_current_inv_slot(1)
        elif self.pressed_2:
            self.player.set_current_inv_slot(2)
        elif self.pressed_3:
            self.player.set_current_inv_slot(3)
        elif self.pressed_4:
            self.player.set_current_inv_slot(4)

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

        if not self.player.get_two_handed():
            # for changing selected inventory slots
            if key == arcade.key.KEY_1:
                self.pressed_1 = True
            elif key == arcade.key.KEY_2:
                self.pressed_2 = True
            elif key == arcade.key.KEY_3:
                self.pressed_3 = True
            elif key == arcade.key.KEY_4:
                self.pressed_4 = True

        # self.process_keychange() # since these are already in on_update I think this is fine to not be here

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

        if not self.player.get_two_handed():
            if key == arcade.key.KEY_1:
                self.pressed_1 = False
            elif key == arcade.key.KEY_2:
                self.pressed_2 = False
            elif key == arcade.key.KEY_3:
                self.pressed_3 = False
            elif key == arcade.key.KEY_4:
                self.pressed_4 = False

        # self.process_keychange()

    def center_camera_to_player(self):
        """
        Needed for centering the camera to the player on each game tick
        """
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (self.camera.viewport_height / 2)

        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered, 0.2)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # Process movement based on keys
        self.process_keychange()

        # Update Animations - this requires an update_animation function in each class.
        # This is pretty straightforward to do and setup, and is worthwhile to do
        # self.scene.update_animation(
        #     delta_time,
        #     [
        #         LAYER_NAME_COINS,
        #         LAYER_NAME_BACKGROUND,
        #         LAYER_NAME_PLAYER,
        #         LAYER_NAME_ENEMIES,
        #     ],
        # )

        # Update walls, used with moving platforms (may not be needed)
        # self.scene.update(self.walls)

        # handle collisions - like this
        item_hit_list = arcade.check_for_collision_with_list(
            self.player, self.loot_items # may need to change layer name
        )
        # Handle checking if items are in hitbox and the player is attempting to pick something up
        # Add the item to inventory if the player's current slot is open
        if self.try_pickup_item and not self.player.get_inv(self.player.get_current_inv_slot()):
            # Since we can only populate the player's inventory slot with a single item,
            # we will only try with the first item
            item_hit_list = arcade.check_for_collision_with_list(self.player, self.loot_items)
            if len(item_hit_list) > 0:
                temp_item = item_hit_list[0]

                self.player.add_item(self.player.get_current_inv_slot(), temp_item)
                self.loot_items.remove(item_hit_list[0]) # I'm not too sure how well this will work, have to try later
                item_hit_list[0].remove_from_sprite_lists() # remove from sprite list too

        # Handle checking if the player wants to drop items
        if self.drop_item and self.player.get_inv(self.player.get_current_inv_slot()):
            temp_item = self.player.remove_item(self.player.get_current_inv_slot())

            # Currently I will be including all of this, I'm not sure if we need to have both
            self.loot_items.append(temp_item)

        # Position the camera
        self.center_camera_to_player()


def main():
    """
    Main function
    """


    # Initialize game and begin runtime
    window = LethalGame()
    window.setup()
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


"""
Current glitches:
- after picking up an item, dropping it, and picking it up again, the sprite in the inventory is not displayed
"""