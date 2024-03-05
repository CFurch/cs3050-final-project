import arcade
import random
import json
from utility_functions import calculate_direction_vector

# half of turret sweep
ANGLE_FROM_DEFAULT = 90
DELAY_TIME_END_OF_SWEEP = 20


class Mine(arcade.Sprite):
    def __init__(self):
        """
        Basic initialization
        """

        # initialize seed
        super().__init__()

        self.weight = 0
        self.texture = None
        self.damage = 100
        self.armed = False
        self.exploded = False
        self.explosion_delay = 10
        self.explosion_distance = 100

    def setup(self, center_x, center_y):
        """
        Load texture and place onto map
        :return: self
        """
        # Load texture from mine file
        self.texture = arcade.load_texture("resources/hazard_sprites/mine.png")
        self.center_x = center_x
        self.center_y = center_y

        return self

    def get_weight(self):
        return self.weight

    def arm_mine(self):
        self.armed = True

    def explode_mine(self):
        self.exploded = True

    def get_armed(self):
        return self.armed

    def get_exploded(self):
        return self.exploded

    def get_damage(self):
        return self.damage

    def get_explosion_distance(self):
        return self.explosion_distance

    def decrease_delay(self):
        """
        Decrease the delay before explosion
        :return:
        """
        self.explosion_delay -= 1
        if self.explosion_delay == 0:
            self.exploded = True


class Turret(arcade.Sprite):
    def __init__(self):
        """
        Basic initialization
        """

        # initialize seed
        super().__init__()

        self.damage = 40
        self.base_direction = None
        self.facing_direction = None
        self.texture = None
        self.scale = 1.0  # Initial scale
        self.rotate_speed = 0.65
        self.rotate_direction = 1
        self.lower_end = None
        self.higher_end = None
        self.delay_at_edges = DELAY_TIME_END_OF_SWEEP
        self.delaying = False

    def setup(self, center_x, center_y, view_direction):
        """
        Load texture and place onto map
        :return: self
        """
        # Load texture from mine file
        self.texture = arcade.load_texture("resources/hazard_sprites/turret.png")
        self.center_x = center_x
        self.center_y = center_y
        self.base_direction = calculate_direction_vector(view_direction)
        self.facing_direction = self.base_direction
        self.lower_end = self.base_direction - ANGLE_FROM_DEFAULT
        self.higher_end = self.base_direction + ANGLE_FROM_DEFAULT
        return self

    def rotate(self, angle_degrees):
        """
        Rotate the turret's texture by the specified angle in degrees.
        """
        self.angle = angle_degrees

    def get_angle(self):
        return self.facing_direction

    def update(self):
        """
        Update turret rotation.
        """
        if not self.delaying:
            # Update the current facing direction based on direction and speed
            self.facing_direction += self.rotate_direction * self.rotate_speed
            # if angle is at end, spin
            if self.facing_direction <= self.lower_end or self.facing_direction >= self.higher_end:
                self.rotate_direction *= -1
                self.delaying = True

        else:
            if self.delay_at_edges != 0:
                self.delay_at_edges -= 1
            else:
                self.delaying = False
                self.delay_at_edges = DELAY_TIME_END_OF_SWEEP


    def draw_scaled(self):
        """
        Draw the turret with scaled texture and rotation.
        """

        arcade.draw_texture_rectangle(self.center_x, self.center_y, self.texture.width * self.scale,
                                      self.texture.height * self.scale, self.texture, self.facing_direction)
