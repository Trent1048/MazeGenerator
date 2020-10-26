from PIL import Image
import numpy as np
from random import randint
from disjointSet import DisjointSet
from mazeSpace import *

def generateMaze(mazeSize, imageSize):

    # get a list of what walls should be drawn
    mazeList = calculateMaze(mazeSize)

    # draw it as an image
    drawMaze(mazeList, mazeSize, imageSize, 'maze.png')

    return mazeList

def drawMaze(mazeList, mazeSize, imageSize, imageName):

    # setup an array for image creation
    data = np.zeros((mazeSize, mazeSize, 3), dtype=np.uint8)

    # fill the image in based on the mazeList
    for row in range(mazeSize):
        for col in range(mazeSize):

            currentSpace = mazeList[row][col].spaceType

            if currentSpace == SpaceType.space:
                data[row, col] = [255, 255, 255]
            elif currentSpace == SpaceType.solvedSpace:
                data[row, col] = [0, 255, 0]
            else:
                data[row, col] = [0, 0, 0]

    # turn the array into an image and save it
    img = Image.fromarray(data, 'RGB')
    img = img.resize((imageSize, imageSize), 0)
    img.save(imageName)
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

def solveMaze(mazeList, mazeSize, imageSize):

    # store neigboring spaces of all open spaces within the maze
    for row in range(mazeSize):
        for col in range(mazeSize):
            currentSpace = mazeList[row][col]

            if currentSpace.spaceType == SpaceType.space:
                currentSpace.neighbors = []

                # search surrounding spaces
                for space in [[row - 1, col], [row + 1, col], [row, col - 1], [row, col + 1]]:
                    # make sure space isn't outside the list
                    if 0 <= space[0] < mazeSize and 0 <= space[1] < mazeSize:
                        spaceBeingSearched = mazeList[space[0]][space[1]]
                        if spaceBeingSearched.spaceType == SpaceType.space:
                            currentSpace.neighbors.append(spaceBeingSearched)

    # setup variables for solving the maze
    startingSpace = mazeList[0][1]
    endSpace = mazeList[mazeSize - 1][mazeSize - 2]
    searchedSpaces = [startingSpace]
    spaceStack = [startingSpace]

    while len(spaceStack) > 0:
        currentSpace = spaceStack.pop()

        # if the current space is the end
        if currentSpace == endSpace:
            break

        # add neighboring spaces to the stack to be checked
        for space in currentSpace.neighbors:
            if not space in searchedSpaces:
                searchedSpaces.append(space)
                spaceStack.append(space)
                space.parentSpace = currentSpace

    # backtrack and mark all parent spaces that got to the end
    while currentSpace != None:
        currentSpace.spaceType = SpaceType.solvedSpace
        currentSpace = currentSpace.parentSpace

    # draw the maze
    drawMaze(mazeList, mazeSize, imageSize, 'mazeSolution.png')

if __name__ == "__main__":
    while True:
        # get inputs
        while True:
            sizeIn = input("How large should the maze be? ")
            try:
                size = abs(int(sizeIn))

                if size < 3:
                    size = 3

                break
            except:
                print("Invalid input")
        while True:
            imageSizeIn = input("How large should the image be? ")
            try:
                imageSize = abs(int(imageSizeIn))

                if imageSize < size:
                    imageSize = size

                break
            except:
                print("Invalid input")

        print("Please wait... ")

        # make sure the maze size is odd so it won't generate wierd
        mazeSize = size
        if mazeSize % 2 == 0:
            mazeSize += 1

        # generate the maze based on the input
        mazeList = generateMaze(mazeSize, imageSize)

        # solve the maze if the user wants
        displaySolution = input("Do you want to see the solution? ")
        if displaySolution.lower().startswith("y"):
            print("Please wait... ")
            solveMaze(mazeList, mazeSize, imageSize)

        # check if the user wants to continue
        keepGoingIn = input("Do you want to go again? ")
        if not keepGoingIn.lower().startswith("y"):
            break