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
        self.mines = None
        self.turrets = None

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

        self.player_start_x = 0
        self.player_start_y = 0

    def setup(self):
        """
        Calculates the map_array and
        :return:
        """
        # Procgen of map:
        player_start, map = test_map()  # generate_map()

        # Scale up player_start
        self.player_start_x = player_start[0] * 256 + 128
        self.player_start_y = player_start[1] * 256 + 128

        self.mines = arcade.SpriteList()
        self.turrets = arcade.SpriteList()

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
                if temp_room.get_hazards()[0] != None:
                    self.mines.extend(temp_room.get_hazards()[0])
                if temp_room.get_hazards()[1] != None:
                    self.turrets.extend(temp_room.get_hazards()[1])
                # Update positions
                x_temp += ROOM_SIZE
            x_temp = HALF_ROOM_SIZE
            y_temp += ROOM_SIZE

    def get_walls(self):
        return self.wall_list

    def get_loot_list(self):
        return self.loot_list

    def get_player_start(self):
        return self.player_start_x, self.player_start_y

    def get_mines(self):
        return self.mines

    def get_turrets(self):
        return self.turrets


def create_grid(map_size):
    
    grid = []

    for y in range(map_size):
        grid.append([])
        for x in range(map_size):
            grid[y].append("0000")

    return grid


def gen_dfs_maze(map_size, seed=0, starting_node=-1):

    # initialize the maze with the map size
    maze = create_grid(map_size)

    # use the provided seed
    random.seed(seed)

    # if another starting node is not provided, use the halfway node along the left side
    if starting_node == -1:
        start_x = 0
        start_y = map_size//2
        starting_node = [start_x, start_y]

    steps = 0

    # initialize lists for maze generation
    visited_nodes = []
    visit_queue = []
    current_node = starting_node
    
    # get possible neighbors of a node in room_id notation
    def get_neighbors(node):

        # get the x/y coordinates
        x = node[0]
        y = node[1]

        # assume all possible
        neighbors = [[x,y+1],[x+1,y],[x,y-1],[x-1,y]]

        # establish bounds
        if x == 0:
            neighbors[3] = 0
        if x == map_size:
            neighbors[1] = 0
        if y == 0:
            neighbors[2] = 0
        if y == map_size:
            neighbors[0] = 0

        # clear all invalid transitions
        neighbors = [node for node in neighbors if node != 0]
        
        return neighbors


    # while the number of visited nodes is less than the maximum number of cells
    while len(visited_nodes) < pow(map_size+1,2):
        # add the current node to the visited nodes list if not already in it
        if current_node not in visited_nodes: visited_nodes.append(current_node)
        
        # DEBUG, REMOVE LATER
        print(steps)
        steps += 1
        print(current_node)
        print(visited_nodes)

        # store current coordinates for reference
        x = current_node[0]
        y = current_node[1]

        # get neighbor absolute positions
        neighbors = get_neighbors(current_node)

        # randomize neighbor ordering
        random.shuffle(neighbors)

        # 
        current_node = neighbors[0]

        
def test_map():
    return  [0,1], [[['0110', [[1, 0, 0], [0, 2, 0]], [[1], [0]], 0],  # y = 0, x = 0
                    ['0101', [[0, 0, 0], [0, 0, 1]], [[0], [1]], 0],  # y = 0, x = 1
                    ['0011', [[1, 0, 0], [0, 0, 0]], [[0], [0]], 0]],  # y = 0, x = 2
                    [['1111', [[0, 0, 0], [0, 0, 0]], [[0], [1]], 0],  # y = 1, x = 0
                    ['0001', [[2, 0, 0], [1, 0, 0]], [[2], [0]], 0],  # y = 1, x = 1
                    ['0010', [[2, 0, 0], [0, 0, 0]], [[0], [0]], 0]],  # y = 1, x = 2
                    [['1100', [[3, 0, 0], [0, 0, 1]], [[0], [1]], 0],  # y = 2, x = 0
                    ['0101', [[0, 0, 2], [0, 1, 0]], [[1], [0]], 0],  # y = 2, x = 1
                    ['1001', [[0, 0, 0], [1, 0, 0]], [[0], [0]], 0]]]  # y = 2, x = 2
