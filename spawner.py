"""
    Note from Colin:
    I'm electing to simplify the spawn mechanics as we do not need the complexity that LC has.
    Spawners will be initialized with the map, and will be given both their monster and their delay for spawn at
    the beginning of the game, and will then use the in-game time to determine when the monster will be released.
    Indoor and Outdoor power will be used on map init to determine what can be spawned.
"""


import arcade
import json

class Spawner(arcade.Sprite):

    def __init__(self):
        """
        initialize monster and time
        """