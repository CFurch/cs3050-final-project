import arcade
import random
import json
from room import Room

ROOM_SIZE = 256
HALF_ROOM_SIZE = 128


class Map(arcade.Sprite):
    def __init__(self, moon_id, seed):
        """
        takes moon_id and optional seed and prepares data for setup
        """

        # initialize seed
        super().__init__()

        # initialize map_array for later
        self.map_array = arcade.SpriteList()

        # moon_data to receive from file
        self.size = 0
        self.difficulty = 0
        self.loot_quantity = []
        self.loot_weight = []
        self.hazards = []

        self.seed = seed
        random.seed = self.seed

        # grab all moon_data from file
        with open("resources/moons.json", 'r') as moon_file:
            moon_data = json.load(moon_file)

        # grab specific moon data and store it in the object
        print(moon_data)
        for moon in moon_data:
            if moon.get("id") == moon_id:
                self.size = moon.get("size")
                self.difficulty = moon.get("difficulty")
                self.loot_quantity = moon.get("loot-quantity")
                self.loot_weight = moon.get("loot-weight")
                self.hazards = moon.get("hazards")

        self.loot_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.hazards = arcade.SpriteList()
        self.spawners = arcade.SpriteList()

    def setup(self):
        """
        Calculates the map_array and
        :return:
        """
        # Procgen of map:
        map = test_map()  # generate_map()
        # determine where to spawn loot on the map

        # determine where to spawn spawners on the map

        # determine where to spawn hazards
        # Both of the above functions will use the procgen results to determine which rooms to spawn

        # Iterate through each room in the representation of the map and create a room
        x_temp = HALF_ROOM_SIZE
        y_temp = HALF_ROOM_SIZE
        # Switch y direction
        for y in range(len(map) - 1, -1, -1):
            row = map[y]
            for x, item in enumerate(row):
                print(x_temp, y_temp, item)
                # generate room based on bitwise rep, x, y, to_spawn_loot, etc
                bitwise_room_rep = item[0]
                # item list, hazards spawned, spawners spawned
                items_to_spawn = item[1]
                hazards = item[2]
                spawners = item[3]
                # Generate room using Room().setup

                temp_room = Room().setup(bitwise_room_rep, x_temp, y_temp, spawners=spawners,
                                         hazards=hazards, loot_item_spawn_list=items_to_spawn)
                # Add each room to the spritelist
                if temp_room.get_loot_list() != None:
                    self.loot_list.extend(temp_room.get_loot_list())
                if temp_room.get_walls() != None:
                    self.wall_list.extend(temp_room.get_walls())
                # Update positions
                x_temp += ROOM_SIZE
            x_temp = HALF_ROOM_SIZE
            y_temp += ROOM_SIZE

    def get_walls(self):
        return self.wall_list

    def get_loot_list(self):
        return self.loot_list


def create_grid(map_size):
    
    grid = []

    for y in range(map_size):
        grid.append([])
        for x in range(map_size):
            grid[y].append("0000")

    return grid


def gen_maze(map_size, seed, starting_node=-1):
    maze = create_grid(map_size)

    random.seed = seed

    # default starting node
    if starting_node == -1:
        start_x = 0
        start_y = map_size//2
        starting_node = [0,start_y]


    visited_nodes = []

    # while the number of visited nodes is less than the maximum number of cells
    # add the current node to the visited nodes list (unique)
    # check available neighbors of the starting node
    # if no neighbors are available, set the current node to the last visited node
    # randomly choose one of the available neighbors
    # update the current cell, and that neighbor
    # change the current node to the neighbor node
        


def test_map():
    return [[['0110', [[1, 0, 0], [0, 2, 0]], [[1], [0]], 0],  # y = 0, x = 0
             ['0101', [[0, 0, 0], [0, 0, 1]], [[0], [1]], 0],  # y = 0, x = 1
             ['0011', [[1, 0, 0], [0, 0, 0]], [[0], [0]], 0]],  # y = 0, x = 2
            [['1111', [[0, 0, 0], [0, 0, 0]], [[0], [1]], 0],  # y = 1, x = 0
             ['0001', [[2, 0, 0], [1, 0, 0]], [[2], [0]], 0],  # y = 1, x = 1
             ['0010', [[2, 0, 0], [0, 0, 0]], [[0], [0]], 0]],  # y = 1, x = 2
            [['1100', [[3, 0, 0], [0, 0, 1]], [[0], [1]], 0],  # y = 2, x = 0
             ['0101', [[0, 0, 2], [0, 1, 0]], [[1], [0]], 0],  # y = 2, x = 1
             ['1001', [[0, 0, 0], [1, 0, 0]], [[0], [0]], 0]]]  # y = 2, x = 2
