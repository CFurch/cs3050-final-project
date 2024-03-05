import arcade
import random
import json
import utility_functions

# half of turret sweep
ANGLE_FROM_DEFAULT = 89  # To handle an bug with turret rotation
DELAY_TIME_END_OF_SWEEP = 20
AGRO_DETECTION_ANGLE = 45
BASE_DETECTION_ANGLE = 30


class Mine(arcade.Sprite):
    def __init__(self):
        """
        Basic initialization
        # TODO: Add dropping weight sets off mine
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
        self.detection_angle = 30

    def setup(self, center_x, center_y, view_direction):
        """
        Load texture and place onto map
        :return: self
        """
        # Load texture from mine file
        self.texture = arcade.load_texture("resources/hazard_sprites/turret.png")
        self.center_x = center_x
        self.center_y = center_y
        self.base_direction = utility_functions.calculate_direction_vector_negative(view_direction)
        # Initialize starting facing direction to be random direction within 90 degrees
        # from base position
        self.facing_direction = self.base_direction + random.randint(-ANGLE_FROM_DEFAULT, ANGLE_FROM_DEFAULT)
        self.lower_end = self.base_direction - ANGLE_FROM_DEFAULT
        self.higher_end = self.base_direction + ANGLE_FROM_DEFAULT
        print(self.lower_end, self.higher_end)
        return self

    def rotate(self, angle_degrees):
        """
        Rotate the turret's texture by the specified angle in degrees.
        """
        self.angle = angle_degrees

    def get_angle(self):
        return self.facing_direction

    def update_status(self, player):
        """
        Update turret rotation.
        """
        previous_direction = self.facing_direction

        distance_to_player = utility_functions.euclidean_distance([player.center_x, player.center_y], [self.center_x,
                                                                                                       self.center_y])

        # Calculate the angle between the turret's facing direction and the player
        if utility_functions.is_within_facing_direction([self.center_x, self.center_y], self.facing_direction,
                                                        [player.center_x, player.center_y],
                                                        swath_degrees=self.detection_angle):
            # The following if statements handle if the turret passes from 360 to 0 degrees or 180 to -180 degrees
            # Otherwise, the turret jumps from where it was to higher or lower end.
            if self.lower_end > 0 or self.higher_end >= 360:
                player_vector = utility_functions.calculate_direction_vector_negative([player.center_x - self.center_x,
                                                                                       player.center_y - self.center_y])
            else:
                player_vector = utility_functions.calculate_direction_vector_positive([player.center_x - self.center_x,
                                                                                       player.center_y - self.center_y])
            if player_vector - previous_direction > 45:
                player_vector -= 360
            elif previous_direction - player_vector > 45:
                player_vector += 360
            if self.facing_direction < player_vector:
                self.facing_direction += self.rotate_speed * 200 / distance_to_player + self.rotate_speed * distance_to_player / 500
            elif self.facing_direction > player_vector:
                self.facing_direction -= self.rotate_speed * 200 / distance_to_player + self.rotate_speed * distance_to_player / 500

            if self.facing_direction >= self.higher_end:
                self.facing_direction = self.higher_end
                self.delaying = True
                self.rotate_direction = -1
            elif self.facing_direction <= self.lower_end:
                self.facing_direction = self.lower_end
                self.delaying = True
                self.rotate_direction = 1
            self.detection_angle = AGRO_DETECTION_ANGLE

        # Basic Turret movement
        elif not self.delaying:
            # Update the current facing direction based on direction and speed
            self.facing_direction += self.rotate_direction * self.rotate_speed
            # if angle is at end, spin
            if self.facing_direction <= self.lower_end or self.facing_direction >= self.higher_end:
                self.rotate_direction *= -1
                self.delaying = True
            self.detection_angle = BASE_DETECTION_ANGLE

        else:
            # Delaying the turret at the edges of sweep
            if self.delay_at_edges != 0:
                self.delay_at_edges -= 1
            else:
                self.delaying = False
                self.delay_at_edges = DELAY_TIME_END_OF_SWEEP
            self.detection_angle = BASE_DETECTION_ANGLE

    def draw_scaled(self):
        """
        Draw the turret with scaled texture and rotation.
        """

        arcade.draw_texture_rectangle(self.center_x, self.center_y, self.texture.width * self.scale,
                                      self.texture.height * self.scale, self.texture, self.facing_direction)
