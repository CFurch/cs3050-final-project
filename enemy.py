import arcade

class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__()
        #basic enemy attributes
        self.health = 0
        self.power_level = 0
        self.movement_speed = 0
        # Need to update sprites with animations, directions, etc
        self.texture = None
        self.path = None
    #Assigns values to the correct attributes
    def setup(self, health, power_level, movement_speed, texture):
        self.health = health
        self.power_level = power_level
        self.movement_speed = movement_speed
        self.texture = arcade.load_texture(texture)
        self.path = None
    
    #getters
    def get_health(self):
        return self.health
    
    def get_movement_speed(self):
        return self.movement_speed

    def get_power_level(self):
        return self.power_level

    #setters
    def set_health(self, health):
        self.health = health
    
    def set_movement_speed(self, movement_speed):
        self.movement_speed = movement_speed

    def set_power_level(self, power_level):
        self.power_level = power_level
    
    #basic A* Pathfinding
    #Other monsters will overload this method if they use a different Pathfinding system, 
    #ie line of sight
    def Pathfinding(self, wall_list, PlayerCharacter):
        self.path = arcade.astar_calculate_path(self.position, PlayerCharacter.position, wall_list, diagonal_movement=False)


    #Draw method
    def on_draw(self):
        self.texture = arcade.load_texture["sprite_texture.jpg"]

    """#Update method
    def update(self):
        Pathfinding(self, wall_list)
    """

    
