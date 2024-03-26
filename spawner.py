"""
    Note from Colin:
    I'm electing to simplify the spawn mechanics as we do not need the complexity that LC has.
    Spawners will be initialized with the map, and will be given both their monster and their delay for spawn at
    the beginning of the game, and will then use the in-game time to determine when the monster will be released.
    Indoor and Outdoor power will be used on map init to determine what can be spawned.

    How it will work:
    A spawner will generate a QUEUE of monsters when the map is initialized, alongside a timer. 
    At the end of the timer, the spawner will attempt to spawn a monster.
    If the monsters power is greater than the maps remaining indoor power, it fails and will wait for it's next timer.
    If the monsters power is equal to or less than the maps remaining indoor power, the monster will be spawned and it will wait for its next timer.

"""

import arcade

class Spawner(arcade.Sprite):

    def __init__(self):
        """
        initialize spawner and variables
        """
        super().__init__()

        self.cooldown_max = 0
        self.cooldown_current = 0
        self.spawn_queue = []

    def setup(self, cooldown, monsters):
        """
        populate the spawn queue
        """
        self.cooldown_max = cooldown
        self.spawn_queue = monsters
        
    def update_spawner(self, time, current_power):
        """
        increments the spawner cooldown
        """
        self.cooldown_current -= time
        
        # if the cooldown is 0
        # and if the current_power is less than the power of the next monster in the queue
        if self.cooldown_current < 0:
            spawn_monster()
            self.cooldown_current = self.cooldown_max


def spawn_monster():
    """
    called when the current cooldown is hit
    """
