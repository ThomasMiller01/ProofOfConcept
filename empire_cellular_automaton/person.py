from random import randint
import random


class Person:
    def __init__(self, _id, colonyID, colonyName, age, strength, reproductionValue, x, y, color, _map):
        self._id = _id
        self._colonyID = colonyID
        self._colonyName = colonyName
        self._age = age
        self._strength = strength
        self._reproductionValue = reproductionValue
        self.reproductionThreshold = 100
        self.x = x
        self.y = y
        self.color = color
        self._map = _map

    def move(self):
        neighbour = self._map.getRandomNeighbour([self.x, self.y])
        neighbour_state = self._map.getPixelState(neighbour)
        checkForAge = self.checkFor('age')
        checkForReproduction = self.checkFor('reproduction')
        if checkForAge != None:
            return checkForAge
        if neighbour_state == 'water':
            return None
        elif neighbour_state == 'empty' or neighbour_state == self._colonyName:
            self.x = neighbour[0][0]
            self.y = neighbour[0][1]
            self._map.updatePixel(self.x, self.y, self.color)
            if checkForReproduction == 'reproduction':
                mutation = self.getMutation(self._strength)
                return {'age': self._age, 'strength': mutation, 'reproductionValue': self._reproductionValue, 'x': self.x, 'y': self.y}
            else:
                return None
        else:
            # fight
            return None

    def getMutation(self, strength):
        rnd_plus_minus = randint(0, 1)
        rnd_amount = randint(0, 10)
        if rnd_plus_minus == 0:
            return strength + rnd_amount
        elif rnd_plus_minus == 1:
            return strength - rnd_amount

    def checkFor(self, check):
        if check == 'age':
            if self._age > self._strength:
                return 'dead'
            rnd = randint(0, 1) * 0.2
            self._age += rnd
            return None
        elif check == 'reproduction':
            if self._reproductionValue > self.reproductionThreshold:
                self._reproductionValue = 0
                return 'reproduction'
            else:
                rnd = randint(0, 1)
                self._reproductionValue += rnd
                return None
        else:
            return None
