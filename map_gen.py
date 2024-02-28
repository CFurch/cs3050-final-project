# room types
# all possible room ID's can be described with 4 bits
# the following data is as follows:
# [room type, loot, hazard, spawner]

# loot:
# [[low, med, high], # small
#  [low, med, high], # medium
#  [low, med, high]] # large
# the values given are the number of each item to spawn

# hazards:
# [[mines], 
#  [turrets]]
# the values given are the number of hazards to spawn of each type

# spawners:
# [vents] 
# the values given are the number of vents to spawn in the room

# empty example 3x3
empty = [[[0000,[[0,0,0],[0,0,0],[0,0,0]],[[0],[0]],0],
          [0000,[[0,0,0],[0,0,0],[0,0,0]],[[0],[0]],0],
          [0000,[[0,0,0],[0,0,0],[0,0,0]],[[0],[0]],0]],
         [[0000,[[0,0,0],[0,0,0],[0,0,0]],[[0],[0]],0],
          [0000,[[0,0,0],[0,0,0],[0,0,0]],[[0],[0]],0],
          [0000,[[0,0,0],[0,0,0],[0,0,0]],[[0],[0]],0]],
         [[0000,[[0,0,0],[0,0,0],[0,0,0]],[[0],[0]],0],
          [0000,[[0,0,0],[0,0,0],[0,0,0]],[[0],[0]],0],
          [0000,[[0,0,0],[0,0,0],[0,0,0]],[[0],[0]],0]]]

# example 3x3
