from PIL import Image
import numpy as np
from random import randint
from disjointSet import DisjointSet
from mazeSpace import *

def generateMaze(mazeSize, imageSize):

    # make sure the maze size is odd so it won't generate wierd
    if mazeSize % 2 == 0:
        mazeSize += 1

    # get a list of what walls should be drawn
    mazeList = calculateMaze(mazeSize)

    # draw it as an image
    drawMaze(mazeList, mazeSize, imageSize)

def drawMaze(mazeList, mazeSize, imageSize):

    # setup an array for image creation
    data = np.zeros((mazeSize, mazeSize, 3), dtype=np.uint8)

    # fill the image in based on the mazeList
    for row in range(mazeSize):
        for col in range(mazeSize):

            if mazeList[row][col].spaceType == SpaceType.space:
                data[row, col] = [255, 255, 255]
            else:
                data[row, col] = [0, 0, 0]

    # turn the array into an image and save it
    img = Image.fromarray(data, 'RGB')
    img = img.resize((imageSize, imageSize), 0)
    img.save('maze.png')
    img.show()

def calculateMaze(mazeSize):

    mazeList = []
    currentRow = None

    for row in range(mazeSize):
        currentRow = []
        mazeList.append(currentRow)
        for col in range(mazeSize):
            # mark edges
            if row == 0 or col == 0 or row == mazeSize - 1 or col == mazeSize - 1:
                currentRow.append(MazeSpace(SpaceType.edge))
            # mark corners
            elif row % 2 == 0 and col % 2 == 0:
                currentRow.append(MazeSpace(SpaceType.corner))
            # mark walls
            elif row % 2 == 0 or col % 2 == 0 and not (row % 2 == 0 and col % 2 == 0):
                currentRow.append(MazeSpace(SpaceType.wall))
            # mark spaces
            else:
                currentRow.append(MazeSpace(SpaceType.space))

    walls = []
    spaces = []

    # add walls/spaces to their respective lists
    for row in range(mazeSize):
        for col in range(mazeSize):

            currentSpace = mazeList[row][col]
            
            if currentSpace.spaceType == SpaceType.wall:
                walls.append(currentSpace)

                # go through neighboring spaces and add them to the neighbor list if their spaceType is space
                for space in [mazeList[row - 1][col], mazeList[row + 1][col], mazeList[row][col - 1], mazeList[row][col + 1]]:
                    
                    if space.spaceType == SpaceType.space:
                        currentSpace.neighbors.append(space)

                        spaces.append(space)

    disjointSpaceSet = DisjointSet(spaces)

    # pick a wall and get it's neighboring spaces, if they are in different partitions combine and remove the wall

    while len(walls) > 1:
        wallIndex = randint(0, len(walls) - 1)
        wall = walls[wallIndex]

        walls.remove(wall)

        if (disjointSpaceSet.find(wall.neighbors[0]) != disjointSpaceSet.find(wall.neighbors[1])):

            wall.spaceType = SpaceType.space
            disjointSpaceSet.union(wall.neighbors[0], wall.neighbors[1])

    # open the start and end of the maze
    mazeList[0][1].spaceType = SpaceType.space
    mazeList[mazeSize - 1][mazeSize - 2].spaceType = SpaceType.space

    return mazeList

generateMaze(51, 500)