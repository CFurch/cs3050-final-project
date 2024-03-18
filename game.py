"""
CS 3050 Team 5


"""
import sys

import arcade
import math
from room import Room
from map import Map
from player import PlayerCharacter
from item import Item
from utility_functions import euclidean_distance, calculate_direction_vector_negative, is_within_facing_direction
from ship import Ship

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "2D Lethal Company"

# Starting location of the player, and movement constants
PLAYER_START_X = 500
PLAYER_START_Y = 500
MAX_STAM = 100
STAM_DRAIN = 0.17 # set to match game
BASE_MOVEMENT_SPEED = 2
SPRINT_DELAY = 30

# delay for entering and leaving building
ENTER_EXIT_DELAY = 50

GAMESTATE_OPTIONS = {"orbit": 0, "outdoors": 1, "indoors": 2}
SHIP_INTERACTION_OPTIONS = {"lever": 0, "door": 1, "terminal": 2}

TILE_SCALING = 0.5


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
        self.gamestate = GAMESTATE_OPTIONS["orbit"]
        self.indoor_map = None
        self.indoor_walls = None
        self.indoor_main_position = None
        self.indoor_main_bounding_box = None
        self.outdoor_starting_position = None
        self.outdoor_main_position = None

        self.ship = Ship().setup()

        self.outdoor_map = None
        self.outdoor_walls = None
        self.outdoor_main_box = None

        self.player = None
        self.inventory_hud = None

        self.indoor_enemy_entities = None
        self.indoor_enemy_entities = None

        self.indoor_loot_items = None
        self.outdoor_loot_items = arcade.SpriteList()

        self.mines = None
        self.armed_mines = None
        self.turrets = None
        self.bullets = None

        self.indoor_physics_engine = None
        self.outdoor_physics_engine = None
        self.ship_physics_engine = None

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

        self.delay_main_enter_exit = ENTER_EXIT_DELAY

        # Inventory slots
        self.try_pickup_item = False
        self.drop_item = False

        # Set power levels - has to do with spawning mechanics
        self.indoor_power = None  # experimentation-40 levels
        self.outdoor_power = None

    def setup(self):
        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Set up the map, using procgen and the map class (passed in as parameters
        # Ideally this would work using some sort of arcade.load_tilemap(map_name)
        # if we use this we need to use layers for the physics engine, otherwise add
        # all walls to the walls list
        self.indoor_map = Map("experimentation") # Will update later based on start screen inputs
        self.indoor_map.setup()

        # get the walls from the map
        self.indoor_walls = self.indoor_map.get_walls()
        self.indoor_loot_items = self.indoor_map.get_loot_list()
        self.mines = self.indoor_map.get_mines()
        self.armed_mines = arcade.SpriteList()
        self.turrets = self.indoor_map.get_turrets()
        self.bullets = arcade.SpriteList()

        # Again, update later to be from user input
        map_settings = self.indoor_map.get_map_data()
        self.outdoor_map = arcade.Scene.from_tilemap(arcade.load_tilemap(map_settings[0]))
        self.outdoor_starting_position = map_settings[1]
        self.indoor_power = map_settings[2]
        self.outdoor_power = map_settings[3]
        self.indoor_main_bounding_box = map_settings[4]
        self.outdoor_main_position = map_settings[5]

        # Initialize player character
        self.player = PlayerCharacter()
        self.indoor_main_position = self.indoor_map.get_player_start()
        # Add logic for starting location of player (from outdoors)
        self.player.center_x = self.outdoor_starting_position[0]
        self.player.center_y = self.outdoor_starting_position[1]
        # self.player.center_x = -20
        # self.player.center_y = -20
        self.player.set_movement_speed(BASE_MOVEMENT_SPEED)  # speed is pixels per frame

        self.inventory_hud = arcade.SpriteList()
        # Add the four sprite items to the list
        for i in range(4):
            temp_sprite = arcade.Sprite("resources/item_sprites/inventory_box.png", scale=0.55)
            self.inventory_hud.append(temp_sprite)

        # Add enemies to scene - spawner class needs to handle these
        # for enemy in self.enemy_entities:
        #     self.scene.add_sprite(enemy)

        # Add loot items to scene
        # for item in loot_items:
        #     self.item_list.append(item)
        #     self.scene.add_sprite(item)

        # Set background color to be black
        arcade.set_background_color(arcade.color.DARK_GRAY)

        # Create indoor physics engine - we can use the platformer without gravity to get the intended effect
        self.indoor_physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, walls=self.indoor_walls
        )
        self.indoor_physics_engine.gravity_constant = 0

        # Create outdoor physics engine - we can use the platformer without gravity to get the intended effect
        self.outdoor_physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.outdoor_map["walls"]
        )
        self.outdoor_physics_engine.gravity_constant = 0

        # Separate physics engine for teh ship - can be used outdoors and in orbit
        self.ship_physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.ship.get_walls()
        )
        self.ship_physics_engine.gravity_constant = 0

        self.gamestate = GAMESTATE_OPTIONS["outdoors"] # Change once ship implemented

        # Also change this
        self.ship.update_position(self.outdoor_starting_position[0] - 64, self.outdoor_starting_position[1] - 128)

    def on_draw(self):
        """
        Render the screen
        """
        # Clear the screen
        self.clear()

        # Start the camera
        self.camera.use()

        """
        FUTURE: May need to add another state for landing, to animate the ship
        """

        # Draw the scene depending on indoors or outdoors
        if self.gamestate == GAMESTATE_OPTIONS["orbit"]:
            self.ship.draw_self()
        elif self.gamestate == GAMESTATE_OPTIONS["outdoors"]:
            self.outdoor_map.draw()
            self.ship.draw_self()
            self.outdoor_loot_items.draw()
            # print("outdoors")
        else: # self.gamestate == GAMESTATE_OPTIONS["indoors"] # equivalent expression
            # print("indoors")
            self.indoor_walls.draw()
            for mine in self.mines:
                if not mine.get_exploded():
                    mine.draw()

            for armed_mine in self.armed_mines:
                if armed_mine.get_exploded():
                    # see if the player is within the explosion distance
                    distance = euclidean_distance((self.player.center_x, self.player.center_y),
                                                  (armed_mine.center_x, armed_mine.center_y))
                    if distance <= armed_mine.get_explosion_distance():
                        self.player.decrease_health(armed_mine.get_damage())
                    self.armed_mines.remove(armed_mine)
                else:
                    armed_mine.draw()

            # Draw loot after mines but before turrets
            self.indoor_loot_items.draw()

            # draw bullets and turrets at correct angles
            for bullet in self.bullets:
                bullet.draw_scaled()
            for turret in self.turrets:
                if turret.get_turret_laser() != None:
                    turret.get_turret_laser().draw()
                turret.draw_scaled()

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
        weight_text = f"{int(self.player.get_weight())} lb"

        # Calculate the position for objects relative to the camera's position
        text_x = self.camera.position[0] + 20
        text_y = self.camera.position[1] + SCREEN_HEIGHT - 30

        # Draw the text at the calculated position
        # arcade.draw_text(health_text, text_x, text_y, arcade.csscolor.RED, 18)\
        health_sprite = arcade.Sprite(f"resources/player_sprites/player_health_sprite_{int(self.player.get_health() // 25)}.png", scale=0.75)
        health_sprite.center_x = self.camera.position[0] + 75
        health_sprite.center_y = self.camera.position[1] + SCREEN_HEIGHT - 80
        # health_sprite.alpha = 128 # use this to set opacity of objects
        health_sprite.draw()

        # Stamina representation
        arcade.draw_text(stamina_text, text_x, text_y - 150, arcade.csscolor.ORANGE, 18)
        arcade.draw_text(weight_text, text_x, text_y - 180, arcade.csscolor.ORANGE, 18)

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

        # Adjust speed for outdoors (since for some reason this is twice the speed of orbit and indoors
        if self.gamestate == GAMESTATE_OPTIONS["outdoors"]:
            self.player.set_movement_speed(self.player.get_movement_speed() / 2)

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
        # Handle dead state, reload ship with no loot items
        # if self.player.get_health() == 0:

        # Process movement based on keys
        self.process_keychange()

        # Move the player with the physics engine
        if self.gamestate == GAMESTATE_OPTIONS["outdoors"]:
            self.outdoor_physics_engine.update()
            self.ship.update_ship()
            # This method will auto-update physics engine for if door is open or shut
            self.ship_physics_engine = arcade.PhysicsEnginePlatformer(
                self.player, self.ship.get_walls()
            )
            self.ship_physics_engine.gravity_constant = 0
            self.ship_physics_engine.update()

            # Interact with the ship
            if self.e_pressed:
                ship_action = self.ship.interact_ship(self.player)
                if ship_action == SHIP_INTERACTION_OPTIONS["lever"]:
                    self.gamestate = GAMESTATE_OPTIONS["orbit"]
                    self.ship.change_orbit()
        elif self.gamestate == GAMESTATE_OPTIONS["indoors"]:
            self.indoor_physics_engine.update()
        elif self.gamestate == GAMESTATE_OPTIONS["orbit"]:
            # This method will auto-update physics engine for if door is open or shut
            self.ship_physics_engine = arcade.PhysicsEnginePlatformer(
                self.player, self.ship.get_walls()
            )
            self.ship_physics_engine.gravity_constant = 0
            self.ship_physics_engine.update()
            if self.e_pressed:
                ship_action = self.ship.interact_ship(self.player)
                if ship_action == SHIP_INTERACTION_OPTIONS["lever"]:
                    self.gamestate = GAMESTATE_OPTIONS["outdoors"]
                    self.ship.change_orbit()

        # handle collisions - like this
        # item_hit_list = arcade.check_for_collision_with_list(
        #     self.player, self.loot_items # may need to change layer name
        # )
        self.player.decrease_pd_delay()
        # Handle checking if items are in hitbox and the player is attempting to pick something up
        # Add the item to inventory if the player's current slot is open
        if self.try_pickup_item and not self.player.get_inv(self.player.get_current_inv_slot()) and \
                self.player.get_pd_delay() == 0:
            # Since we can only populate the player's inventory slot with a single item,
            # we will only try with the first item
            if self.gamestate == GAMESTATE_OPTIONS["outdoors"]:
                # Check outdoor loot items
                item_hit_list = arcade.check_for_collision_with_list(self.player, self.outdoor_loot_items)
                if len(item_hit_list) > 0:
                    temp_item = item_hit_list[0]

                    self.player.add_item(self.player.get_current_inv_slot(), temp_item)
                    self.outdoor_loot_items.remove(item_hit_list[0]) # I'm not too sure how well this will work, have to try later
                    item_hit_list[0].remove_from_sprite_lists() # remove from sprite list too
            else:
                # Check indoor loot items
                item_hit_list = arcade.check_for_collision_with_list(self.player, self.indoor_loot_items)
                if len(item_hit_list) > 0:
                    temp_item = item_hit_list[0]

                    self.player.add_item(self.player.get_current_inv_slot(), temp_item)
                    self.indoor_loot_items.remove(
                        item_hit_list[0])  # I'm not too sure how well this will work, have to try later
                    item_hit_list[0].remove_from_sprite_lists()  # remove from sprite list too

        # Handle checking if the player wants to drop items

        if self.drop_item and self.player.get_inv(self.player.get_current_inv_slot()) and \
                self.player.get_pd_delay() == 0:
            temp_item = self.player.remove_item(self.player.get_current_inv_slot())
            if self.gamestate == GAMESTATE_OPTIONS["outdoors"]:
                self.outdoor_loot_items.append(temp_item)
            else:
                self.indoor_loot_items.append(temp_item)

        # Check if a player is on a mine
        if self.gamestate == GAMESTATE_OPTIONS["indoors"]:
            mine_hit_list = arcade.check_for_collision_with_list(self.player, self.mines)
            if len(mine_hit_list) > 0:
                for mine in mine_hit_list:
                    mine.arm_mine()
                    self.mines.remove(mine)
                    self.armed_mines.append(mine)

            # Decrease delay for armed mines not touching the player
            for mine in self.armed_mines:
                if not arcade.check_for_collision(self.player, mine):
                    mine.decrease_delay()

            # Iterate through turrets and update
            for turret in self.turrets:
                turret.update_status(self.player, self.indoor_walls)
                # Need to set this as a temporary variable, as these are wiped from turrets memory by getter
                turret_bullets = turret.get_bullets()
                if len(turret_bullets) > 0:
                    self.bullets.extend(turret_bullets)

            # Will have to change bullets if implement shotguns - allows bullets outside
            # Check for bullet collisions with wall
            for bullet in self.bullets:
                bullet.update()
                bullet_wall_list = arcade.check_for_collision_with_list(
                    bullet, self.indoor_walls
                )
                if len(bullet_wall_list) > 0:
                    self.bullets.remove(bullet)

            # Check for bullet collisions with player, decrement health if hit
            bullet_hit_list = arcade.check_for_collision_with_list(
                self.player, self.bullets
            )
            for bullet in bullet_hit_list:
                # remove from bullets
                self.bullets.remove(bullet)
                self.player.decrease_health(bullet.get_damage())

        # Check for collision with entrances (enter indoors if outside)
        if self.gamestate == GAMESTATE_OPTIONS["outdoors"] and len(arcade.check_for_collision_with_list(self.player, self.outdoor_map["entrance"])) > 0:

            if self.e_pressed:
                if self.delay_main_enter_exit == 0:
                    self.gamestate = GAMESTATE_OPTIONS["indoors"]
                    self.delay_main_enter_exit = ENTER_EXIT_DELAY
                    # Move player to indoors starting position
                    self.player.center_x = self.indoor_main_position[0] - 64
                    self.player.center_y = self.indoor_main_position[1]
                elif self.e_pressed:
                    self.delay_main_enter_exit -= 1
        # Exit if inside
        elif self.gamestate == GAMESTATE_OPTIONS["indoors"] and arcade.check_for_collision(self.player, self.indoor_main_bounding_box):

            if self.e_pressed:
                if self.delay_main_enter_exit == 0:
                    # print("exitting")
                    self.gamestate = GAMESTATE_OPTIONS["outdoors"]
                    self.delay_main_enter_exit = ENTER_EXIT_DELAY
                    # set player to outdoor main position
                    self.player.center_x = self.outdoor_main_position[0]
                    self.player.center_y = self.outdoor_main_position[1]
                else:
                    # print("delaying")
                    self.delay_main_enter_exit -= 1

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