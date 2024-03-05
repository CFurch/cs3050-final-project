import arcade
import random
import json


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
    ANGLE_FROM_DEFAULT = 90

    def __init__(self):
        """
        Basic initialization
        """

        # initialize seed
        super().__init__()

        self.weight = 0
        self.texture = None
        self.damage = 40
        self.base_direction = None

    def setup(self, center_x, center_y, view_direction):
        """
        Load texture and place onto map
        :return: self
        """
        # Load texture from mine file
        self.texture = arcade.load_texture("resources/hazard_sprites/turret.png")
        self.center_x = center_x
        self.center_y = center_y
        self.base_direction = view_direction
        print(self.base_direction)
        return self
