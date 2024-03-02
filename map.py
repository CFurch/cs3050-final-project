import arcade
import random
import json


class Map(arcade.Sprite):

    # variables
    seed = 0

    # initialize map_array for later
    map_array = []
    
    # moon_data to receive from file
    size = 0
    difficulty = 0
    loot_quantity = []
    loot_weight = []
    hazards = []
    
    def __init__(self):
        """
        This needs to have an overall wall list, created when making all the rooms together.
        the Room class needs to implement a Room.get_walls method for this
        """

    def __init__(self, moon_id, seed):
        """
        takes moon_id and optional seed and prepares data for setup
        """

        # initialize seed
        self.seed = seed
        random.seed = self.seed

        # grab all moon_data from file
        with open("resources/moons.json",'r') as moon_file:
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



    def setup(self, procgen_results):
        """
        Calculates the map_array and
        :return:
        """
        # determine where to spawn loot on the map

        # determine where to spawn spawners on the map

        # determine where to spawn hazards
        # Both of the above functions will use the procgen results to determine which rooms to spawn

        # Iterate through each room in the representation of the map and create a room
        # for room in map
        #      generate room based on bitwise rep, x, y, to_spawn_loot, etc
        #      get room object and sub-objects, including the walls list, loot items spawned,
        #      hazards spawned, spawners spawned
        #      add each of these things to the lists of items with that
        # return each of the lists

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
    return [[['0110',[[[1,0,0],[0,2,0]],[[1],[0]],0], # y = 0, x = 0
             ['0101',[[0,0,0],[0,0,1]],[[0],[1]],0], # y = 0, x = 1
             ['0011',[[1,0,0],[0,0,0]],[[0],[0]],0]], # y = 0, x = 2
            [['1111',[[0,0,0],[0,0,0]],[[0],[1]],0], # y = 1, x = 0
             ['0001',[[2,0,0],[1,0,0]],[[2],[0]],0], # y = 1, x = 1
             ['0010',[[2,0,0],[0,0,0]],[[0],[0]],0]], # y = 1, x = 2
            [['1100',[[3,0,0],[0,0,1]],[[0],[1]],0], # y = 2, x = 0
             ['0101',[[0,0,2],[0,1,0]],[[1],[0]],0], # y = 2, x = 1
             ['1001',[[0,0,0],[1,0,0]],[[0],[0]],0]]]] # y = 2, x = 2




