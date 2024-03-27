import arcade

class Enemy(arcade.Sprite):
    #initializtion function
    def __init__(self):
        super().__init__()

        #basic enemy attributes
        self.health = 0
        self.power_level = 0
        self.movement_speed = 0
        self.type = None
        self.barrier_list = None

        # Need to update sprites with animations, directions, etc
        self.texture = None
        self.texture_map = None
        self.path = None

    #Assigns values to the correct attributes
    def setup(self, health, power_level, Type, movement_speed, texture, wall_list):
        self.health = health
        self.type = Type
        self.path = None
        self.barrier_list = wall_list

        # Load item data from JSON
        with open("resources/monsters.json", "r") as file:
            data_from_json = json.load(file)

            #Assuming that type is the same as the identifiers for monsters.json
            self.power_level = self.type["power"]
            self.movement_speed = self.type["movement_speed"]
            self.texture = arcade.sprite(self.type["sprite"])
            self.texture = arcade.load_texture(self.type["sprite"])

        file.close()

        return self
    
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
    def Pathfinding(self, PlayerCharacter):
        self.path = arcade.astar_calculate_path(self.position, PlayerCharacter.position, self.wall_list, diagonal_movement=False)


    #Draw method
    def draw_self(self):
        self.texture_map.center_x = self.center_x
        self.texture_map.center_y = self.center_y
        self.texture_map.draw()

    #Update method
    def update(self):
        Pathfinding(self, PlayerCharacter)
    

    
