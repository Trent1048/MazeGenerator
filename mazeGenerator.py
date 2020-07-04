from PIL import Image
import numpy as np

def generateMaze(mazeSize, imageSize):

    # make sure the maze size is odd so it won't generate wierd
    if mazeSize % 2 == 0:
        mazeSize += 1

    data = np.zeros((mazeSize, mazeSize, 3), dtype=np.uint8)

    # create a grid
    for i in range(mazeSize):
        for j in range(mazeSize):

            if i != 0 and j != 0 and i != mazeSize - 1 and j != mazeSize - 1 and i % 2 != 0 and j % 2 != 0:
                data[i, j] = [255, 255, 255]

    # turn the array into an image and save it
    img = Image.fromarray(data, 'RGB')
    img = img.resize((imageSize, imageSize), 0)
    img.save('maze.png')
    img.show()

generateMaze(10, 500)