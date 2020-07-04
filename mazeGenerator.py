from PIL import Image
import numpy as np
import random

def generateMaze(mazeSize, imageSize):

    # make sure the maze size is odd so it won't generate wierd
    if mazeSize % 2 == 0:
        mazeSize += 1

    # setup an array for image creation and fill it with white
    data = np.zeros((mazeSize, mazeSize, 3), dtype=np.uint8)
    data[0:mazeSize, 0:mazeSize] = [255, 255, 255]

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
                # (the disjoint set will be implimented later, random is a placeholder)
                if random.random() > 0.5:
                    data[row, col] = [0, 0, 0]

    # turn the array into an image and save it
    img = Image.fromarray(data, 'RGB')
    img = img.resize((imageSize, imageSize), 0)
    img.save('maze.png')
    img.show()

generateMaze(11, 500)