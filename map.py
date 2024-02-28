import arcade


class Map(arcade.Sprite):
    def __init__(self):
        """
        This needs to have an overall wall list, created when making all the rooms together.
        the Room class needs to implement a Room.get_walls method for this
        """

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



