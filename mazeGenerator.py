from PIL import Image
import numpy as np
from random import randint
from disjointSet import DisjointSet

def generateMaze(mazeSize, imageSize):

    # make sure the maze size is odd so it won't generate wierd
    if mazeSize % 2 == 0:
        mazeSize += 1

    # setup an array for image creation and fill it with white
    data = np.zeros((mazeSize, mazeSize, 3), dtype=np.uint8)
    data[0:mazeSize, 0:mazeSize] = [255, 255, 255]

    # get a list of what walls should be drawn and keep track of the current one
    wallList = calculateWalls(mazeSize)
    currentWall = 0

    # draw black on the boarders and walls of the maze
    for row in range(mazeSize):
        for col in range(mazeSize):

            # make edges black
            if row == 0 or col == 0 or row == mazeSize - 1 or col == mazeSize - 1:
                data[row, col] = [0, 0, 0]
            # make intersections of walls black
            elif row % 2 == 0 and col % 2 == 0:
                data[row, col] = [0, 0, 0]
            # go through walls
            elif row % 2 == 0 or col % 2 == 0 and not (row % 2 == 0 and col % 2 == 0):
                # color them based on earlier calculations using a disjoint set
                if wallList[currentWall]:
                    data[row, col] = [0, 0, 0]
                
                currentWall += 1

    # turn the array into an image and save it
    img = Image.fromarray(data, 'RGB')
    img = img.resize((imageSize, imageSize), 0)
    img.save('maze.png')
    img.show()

def calculateWalls(mazeSize):

    # figure out how many walls there are
    mainWallPortion = (mazeSize - 1) / 2
    otherWallPortion = mainWallPortion - 1
    wallPortionAmount = (mazeSize - 3) / 2

    wallCount = (int)(wallPortionAmount * (mainWallPortion + otherWallPortion) + otherWallPortion)

    walls = []

    for wall in range(wallCount):
        walls.append(True)

    # do disjoint set calculations
    wallIndexList = []
    for wall in range(wallCount):
        wallIndexList.append(wall)

    disjointWallSet = DisjointSet(wallIndexList)

    # pick 2 random, if they are in different partitions combine and remove wall, if in same partition remove from list

    while len(wallIndexList) > 1:
        wall1Index = randint(0, len(wallIndexList) - 1)
        wall1 = wallIndexList[wall1Index]

        wallIndexList.remove(wall1)

        wall2Index = randint(0, len(wallIndexList) - 1)
        wall2 = wallIndexList[wall2Index]

        if (disjointWallSet.find(wall1) != disjointWallSet.find(wall2)):

            walls[wall1] = False
            disjointWallSet.union(wall1, wall2)

    return walls

generateMaze(11, 500)