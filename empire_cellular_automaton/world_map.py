import numpy as np
from random import randint
import pygame
from settings import *


class Map:
    def __init__(self, img, colonys):
        # init colorCodes for getPixelState()
        self.colorCodes = {str(world_pixel['water']): 'water', str(
            world_pixel['empty']): 'empty'}
        # add foreach colony the colonys color code
        for colony in colonys:
            self.colorCodes[str(colony[1])] = colony[0]

        # load image
        self._image = pygame.image.load(img)

        # get 3d pixel array
        self._pixel_arr = pygame.surfarray.array3d(self._image)

        # set image dimensions
        self.h = self._pixel_arr.shape[0]
        self.w = self._pixel_arr.shape[1]

        # set earth pixel nmb for getColorPercentage()
        nmb = 0
        for x in self._pixel_arr:
            for y in x:
                if y.item(0) == world_pixel['empty'][0] and y.item(1) == world_pixel['empty'][1] and y.item(2) == world_pixel['empty'][2]:
                    nmb += 1
        self.land_pixel_nmb = nmb

        self.updateMap()

    def updateMap(self):
        # map
        pass

    def updateStats(self, stats):
        # stats
        pass

    def updatePixel(self, x, y, color):
        # set pixel color
        self._pixel_arr[x, y] = color

    def getRandomNeighbour(self, pixel):
        x = -1
        y = -1
        # while pixel is in the dimensions of the image
        while x <= 0 or x >= self.w and y <= 0 or y >= self.h:
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
        return [[x, y], self._pixel_arr[x, y]]

    def getPixelState(self, pixel):
        # check pixel color in colorCodes
        # if it does not exist, return "undefinded"
        if str(pixel[1].tolist()) not in self.colorCodes:
            return "undefinded"
        else:
            # else return pixel state name
            return self.colorCodes[str(pixel[1].tolist())]

    def getColorPercentage(self, color):
        allColor = []
        # foreach pixel
        for x in self._pixel_arr:
            for y in x:
                # if pixel matches color append pixel to allColor
                if y.item(0) == color[0] and y.item(1) == color[1] and y.item(2) == color[2]:
                    allColor.append([[x, y], color])
        allColorNmb = allColor.__len__()
        # calculate percentage
        percentage = allColorNmb / self.land_pixel_nmb * 100
        return round(percentage)
