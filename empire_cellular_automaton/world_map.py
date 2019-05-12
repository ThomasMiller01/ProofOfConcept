import cv2
import numpy
from random import randint


class Map:
    def __init__(self, img, colonys):
        self.colorCodes = {'[168, 0, 3]': 'water', '[0, 124, 5]': 'empty'}
        for colony in colonys:
            self.colorCodes[str(colony[1])] = colony[0]
        self.map_image = cv2.imread(img)
        self.h = self.map_image.shape[0]
        self.w = self.map_image.shape[1]

        # for i in range(0, self.h):
        #     for j in range(0, self.w):
        #         rgb = self.map_image[i, j].tolist()

        cv2.imshow('image', self.map_image)

    def getRandomNeighbour(pixel):
        x = -1
        y = -1
        while x <= 0 and x >= self.w and y <= 0 and y >= self.h:
            rnd = randint(0, 7)
            if rnd == 0:  # oben
                x = pixel[0]
                y = pixel[1] + 1
            elif rnd == 1:  # oben rechts
                x = pixel[0] + 1
                y = pixel[1] + 1
            elif rnd == 2:  # rechts
                x = pixel[0] + 1
                y = pixel[1]
            elif rnd == 3:  # unten rechts
                x = pixel[0] + 1
                y = pixel[1] - 1
            elif rnd == 4:  # unten
                x = pixel[0]
                y = pixel[1] - 1
            elif rnd == 5:  # unten links
                x = pixel[0] - 1
                y = pixel[1] - 1
            elif rnd == 6:  # links
                x = pixel[0] - 1
                y = pixel[1]
            elif rnd == 7:  # oben links
                x = pixel[0] - 1
                y = pixel[1] + 1
        self.map_image(y, x)

    def getPixelState(self, pixel):
        return self.colorCodes[str(self.map_image[pixel[0], pixel[1]])]
