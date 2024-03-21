import arcade
import random
import json
from room import Room
import time

ROOM_SIZE = 256
HALF_ROOM_SIZE = 128
MAP_SIZE = 10

class Map(arcade.Sprite):
    def __init__(self, moon_id, seed=0):
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
        self.hazard_quantity = []
        self.mines = None
        self.turrets = None
        # previous seed: random.randrange(0,2**31-1)
        self.seed = XORshift(int(time.time()))

        random.seed(self.seed)

        # grab all moon_data from file
        with open("resources/moons.json", 'r') as moon_file:
            moon_data = json.load(moon_file)

        # grab specific moon data and store it in the object
        # print(moon_data)
        for moon in moon_data:
            if moon.get("id") == moon_id:
                self.size = moon.get("size") * MAP_SIZE
                self.difficulty = moon.get("difficulty")
                self.loot_quantity = moon.get("loot-quantity")
                self.loot_weight = moon.get("loot-weight")
                self.hazard_quantity = moon.get("hazards")
                # load outdoor attributes
                self.outdoor_tilemap_name = moon.get("outdoor_tilemap")
                self.outdoor_starting_position = moon.get("outdoor_starting_position", [])
                self.indoor_power = moon.get("indoor_power", int)
                self.outdoor_power = moon.get("outdoor_power", int)
                self.indoor_main_entrance_sprite = moon.get("indoor_main_hit_box", {})
                self.indoor_main_entrance_image = moon.get("indoor_main_image", {})
                self.outdoor_leave_position = moon.get("outdoor_leave_main_position", [])

        self.loot_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.hazards = arcade.SpriteList()
        self.spawners = arcade.SpriteList()

        self.player_start_x = 0
        self.player_start_y = 0

    def setup(self):
        """
        Calculates the map_array and loot spawns
        :return:
        """

        # gen_dfs_maze takes: size and seed
        player_start, maze = gen_dfs_maze(int(self.size) , self.seed)
        map = maze

        # Scale up player_start
        self.player_start_x = player_start[0] * 256 + 128
        self.player_start_y = player_start[1] * 256 + 128

        # Set the indoor main entrance collision box
        temp_sprite = arcade.Sprite(self.indoor_main_entrance_sprite["texture"])
        temp_sprite.center_x = self.indoor_main_entrance_sprite["center_x"] + self.player_start_x
        temp_sprite.center_y = self.indoor_main_entrance_sprite["center_y"] + self.player_start_y
        self.indoor_main_entrance_sprite = temp_sprite

        temp_sprite = arcade.Sprite(self.indoor_main_entrance_image["texture"])
        temp_sprite.center_x = self.indoor_main_entrance_image["center_x"] + self.player_start_x
        temp_sprite.center_y = self.indoor_main_entrance_image["center_y"] + self.player_start_y
        self.wall_list.append(temp_sprite)

        self.mines = arcade.SpriteList()
        self.turrets = arcade.SpriteList()

        # populate the maze with empties
        # for each column in the map
        # for each room in the column
        # add the empty data to the room
        for x, column in enumerate(maze):
            for y, row in enumerate(column):
                new_room = [column[y], [[0,0,0],[0,0,0]],[0,0],0]
                map[x][y] = new_room

        # loot generation
        gen_loot(map, self.loot_quantity, self.loot_weight)

        # hazard generation
        gen_hazards(map, self.hazard_quantity)
    
        # create spawners for monsters

        # Iterate through each room in the representation of the map and create a room
        x_temp = HALF_ROOM_SIZE
        y_temp = HALF_ROOM_SIZE
        # Switch y direction
        for y, col in enumerate(map):
            # row = map[y]
            for x, item in enumerate(col):
                #print(item)
                #print(x_temp, y_temp, item)

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
                y_temp += ROOM_SIZE
            y_temp = HALF_ROOM_SIZE
            x_temp += ROOM_SIZE

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

    def get_map_data(self):
        return self.outdoor_tilemap_name, self.outdoor_starting_position, self.indoor_power, self.outdoor_power, \
               self.indoor_main_entrance_sprite, self.outdoor_leave_position

def create_grid(map_size):
    
    grid = []

    for x in range(map_size):
        grid.append([])
        for y in range(map_size):
            grid[x].append("0000")

    return grid

def gen_dfs_maze(map_size, seed):

    # initialize the maze with the map size
    maze = create_grid(map_size)

    random.seed(seed)

    # assign default starting node
    start_x = 0
    start_y = map_size // 2
    starting_node = [start_x, start_y]

    # initialize lists for maze generation
    visited_nodes = []
    visit_queue = []
    current_node = starting_node
    
    # get possible neighbors of a node in room_id notation
    def get_neighbors(node):

        # get the x/y coordinates
        x = node[0]
        y = node[1]

        # assume all transitions possible
        neighbors = [[x,y+1],[x+1,y],[x,y-1],[x-1,y]]

        # establish bounds
        if x == 0:
            neighbors[3] = 0
        if x == map_size-1:
            neighbors[1] = 0
        if y == 0:
            neighbors[2] = 0
        if y == map_size-1:
            neighbors[0] = 0

        # clear all invalid transitions
        neighbors = [node for node in neighbors if node != 0]
        
        return neighbors
    
    # calculate the room ID based on node positions
    def calc_roomid(source_node, dest_node):
        
        dir_diff = []
        paths = []
        
        # compute X and Y directional differences
        dir_diff.append((dest_node[0] - source_node[0]) + 1)
        dir_diff.append((dest_node[1] - source_node[1]) + 1)

                               #y=-1,y=0,y=1
        direction_decision = [[[0,0],[1,100],[0,0]], # x = -1
                              [[10,1000],[0,0],[1000,10]], # x = 0
                              [[0,0],[100,1],[0,0]]] # x = 1

        paths = direction_decision[dir_diff[0]][dir_diff[1]]
        
        return paths

    # while the number of visited nodes is less than the maximum number of cells
    while len(visited_nodes) < pow(map_size,2):

        # add the current node to the visited nodes list if not already in it
        if current_node not in visited_nodes: visited_nodes.append(current_node)

        # store current_node coordinates
        x = current_node[0]
        y = current_node[1]

        # get available neighbors, and store their information as an absolute position within the maze
        neighbors = get_neighbors(current_node)

        # reset valid neighbors from previous run
        valid_neighbors = []

        # if the neighbor has not been visited, add it to the valid_neighbors list
        for neighbor in neighbors:
            if neighbor not in visited_nodes: valid_neighbors.append(neighbor)

        # randomize valid neighbor ordering
        random.shuffle(valid_neighbors)
        
        # if no neighbors exist, backtrack. 
        # otherwise, append the current node to the visit queue, and update the paths
        if len(valid_neighbors) == 0:
            current_node = visit_queue.pop()

        else: 
            # append the current node to the visit queue
            visit_queue.append(current_node)

            # compute relevant paths
            paths = calc_roomid(current_node,valid_neighbors[0])
           
            # update the current node with the outpath
            maze[x][y] = str(int(maze[x][y]) + int(paths[0])).zfill(4)
            maze[valid_neighbors[0][0]][valid_neighbors[0][1]] = str(int(maze[valid_neighbors[0][0]][valid_neighbors[0][1]]) + 
                                                                     int(paths[1])).zfill(4)
            
            # update the neighbor node with the inpath

            current_node = valid_neighbors[0]

    # create a doorway for the starting node
    maze[start_x][start_y] = str(int(maze[start_x][start_y]) + 1).zfill(4)

    
    # generate random hallways
    total_halls = 0
    while total_halls < (0.75 * pow(map_size,2)):
        rand_x = random.randrange(1, map_size-1)
        rand_y = random.randrange(1, map_size-1)

        dir_population = ["1000","0100","0010","0001"]
        rand_dirr = random.sample(dir_population,1)

        maze[rand_x][rand_y] = str(int(maze[rand_x][rand_y]) + int(rand_dirr[0])).replace("2","1").zfill(4)

        total_halls += 1


    return starting_node, maze

def gen_loot(map, loot_quantity, loot_weight):
    """
    randomly generate the loot from the map
    """

    rand_loot_quant = random.randrange(loot_quantity[0],loot_quantity[1])
    total_loot = 0

    # join loot weights and define population
    loot_population = ['one_low','one_mid','one_high','two_low','two_mid','two_high']
    loot_weights_total = loot_weight['one_handed'] + loot_weight['two_handed']

    # while there is still
    # loot to be placed, randomly select a room and check it's ID
    while total_loot < rand_loot_quant:
        # randomly generate X and Y coordinates within the map bounds
        rand_x = random.randrange(0,len(map))
        rand_y = random.randrange(0,len(map))

        # if the room has transitions
        if map[rand_x][rand_y][0] != "0000":
            # use the weights to calculate what item will spawn
            choice = random.choices(loot_population,loot_weights_total)
            
            match choice[0]:
                case 'one_low':
                    map[rand_x][rand_y][1][0][0] += 1
                case 'one_mid':
                    map[rand_x][rand_y][1][0][1] += 1
                case 'one_high':
                    map[rand_x][rand_y][1][0][2] += 1
                case 'two_low':
                    map[rand_x][rand_y][1][1][0] += 1
                case 'two_mid':
                    map[rand_x][rand_y][1][1][1] += 1
                case 'two_high':
                    map[rand_x][rand_y][1][1][2] += 1

            total_loot += 1

def gen_hazards(map, hazard_quantity):

    # initialize variables
    max_mines = hazard_quantity['mines'][0]
    max_turrets = hazard_quantity['turrets'][0]
    total_mines = 0
    total_turrets = 0

    # while there are still mines and turrets to be placed
    # randomly select a room and check it's ID
    while total_mines < max_mines:
        rand_x = random.randrange(0,len(map))
        rand_y = random.randrange(0,len(map))

        if map[rand_x][rand_y][0] != "0000":
            map[rand_x][rand_y][2][0] += 1
            total_mines += 1

    while total_turrets < max_turrets:
        rand_x = random.randrange(0,len(map))
        rand_y = random.randrange(0,len(map))

        if map[rand_x][rand_y][0] != "0000":
            map[rand_x][rand_y][2][1] += 1
            total_turrets += 1

def gen_spawners(map, indoor_power, monsters):
    """
    Randomly create the spawners for the map alongside their timers and selected monster
    """


def XORshift(state):
    """
    This is for producing a random state
    :param state:
    :return:
    """
    x = state
    x ^= (x << 13) & 0xFFFFFFFF
    x ^= (x >> 17) & 0xFFFFFFFF
    x ^= (x << 5) & 0xFFFFFFFF
    return x

