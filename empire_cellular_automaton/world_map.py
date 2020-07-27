import numpy
from random import randint
import pygame


class Map:
    def __init__(self, img, colonys):
        # init colorCodes for getPixelState()
        self.colorCodes = {'[3, 0, 168]': 'water', '[5, 124, 0]': 'empty'}
        # add foreach colony the colonys color code
        for colony in colonys:
            self.colorCodes[str(colony[1])] = colony[0]

        # init pygame
        pygame.init()

        # load image
        self._image = pygame.image.load(img)

        # get 2d pixel array
        self._pixel_arr = pygame.surfarray.array3d(self._image)

        # set image dimensions
        self.h = self._pixel_arr.shape[0]
        self.w = self._pixel_arr.shape[1]

        # create display surface
        self.display_surface = pygame.display.set_mode((self.h, self.w))

        # set the pygame window name
        pygame.display.set_caption('Empire - Cellular Automaton')

        # completely fill the surface object with white color
        self.display_surface.fill([255, 255, 255])

        # set earth pixel nmb for getColorPercentage()
        nmb = 0
        for x in self._pixel_arr:
            for y in x:
                if y.item(0) == 5 and y.item(1) == 124 and y.item(2) == 0:
                    nmb += 1
        self.land_pixel_nmb = nmb
        # show image
        self.updateMap()

    def updateMap(self):
        surface = pygame.surfarray.make_surface(self._pixel_arr)
        self.display_surface.blit(surface, (0, 0))
        pygame.display.update()

    def updatePixel(self, x, y, color):
        # set pixel color
        self._pixel_arr[x, y].itemset(0, color[0])
        self._pixel_arr[x, y].itemset(1, color[1])
        self._pixel_arr[x, y].itemset(2, color[2])

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
        return [[x, y], self.getPixel(x, y)]

    def getPixel(self, x, y):
        # return pixel of x and y
        return self._pixel_arr[x, y]

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
        # return 0

    # method used for getting x and y value of mouse click
    # def mouse_drawing(self, event, x, y, flags, params):
    #     if event == cv2.EVENT_LBUTTONDOWN:
    #         print("Left click")
    #         print("x, y: ", x, y)
    #         circles.append((x, y))