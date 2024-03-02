import arcade
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
        Generating
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

def generate_map():
    """
    Generate the array representation of the map
    :return:
    """
    
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




