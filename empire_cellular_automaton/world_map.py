import cv2
import numpy
from random import randint


class Map:
    def __init__(self, img, colonys):
        # init colorCodes for getPixelState()
        self.colorCodes = {'[168, 0, 3]': 'water', '[0, 124, 5]': 'empty'}
        # add foreach colony the colonys color code
        for colony in colonys:
            self.colorCodes[str(colony[1])] = colony[0]
        self.map_image = cv2.imread(img)
        # set image dimensions
        self.h = self.map_image.shape[0]
        self.w = self.map_image.shape[1]

        # set earth pixel nmb for getColorPercentage()
        nmb = 0
        for y in range(0, self.h):
            for x in range(0, self.w):
                if self.map_image[y, x].item(0) == 0 and self.map_image[y, x].item(1) == 124 and self.map_image[y, x].item(2) == 5:
                    nmb += 1
        self.land_pixel_nmb = nmb
        # show image
        cv2.namedWindow('image')
        # cv2.setMouseCallback("image", self.mouse_drawing)
        cv2.imshow('image', self.map_image)
        # cv2.waitKey(0)

    def updateMap(self):
        # show image
        cv2.imshow('image', self.map_image)

    def updatePixel(self, x, y, color):
        # set pixel color
        self.map_image[y, x].itemset(0, color[0])
        self.map_image[y, x].itemset(1, color[1])
        self.map_image[y, x].itemset(2, color[2])

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
        return [[x, y], self.map_image[y, x]]

    def getPixel(self, x, y):
        # return pixel of x and y
        return self.map_image[y, x]

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
        for y in range(0, self.h):
            for x in range(0, self.w):
                # if pixel matches color append pixel to allColor
                if self.map_image[y, x].item(0) == color[0] and self.map_image[y, x].item(1) == color[1] and self.map_image[y, x].item(2) == color[2]:
                    allColor.append([[x, y], color])
        allColorNmb = allColor.__len__()
        # calculate percentage
        percentage = allColorNmb / self.land_pixel_nmb * 100
        return round(percentage)

    # method used for getting x and y value of mouse click
    # def mouse_drawing(self, event, x, y, flags, params):
    #     if event == cv2.EVENT_LBUTTONDOWN:
    #         print("Left click")
    #         print("x, y: ", x, y)
    #         circles.append((x, y))
