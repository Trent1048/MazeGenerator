from enum import Enum

class SpaceType(Enum):

    edge = 0
    corner = 1
    space = 2
    wall = 3
    solvedSpace = 4

class MazeSpace:

    def __init__(self, spaceType):
        self.spaceType = spaceType
        self.neighbors = []