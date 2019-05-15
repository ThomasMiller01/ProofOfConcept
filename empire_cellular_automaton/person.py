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
        self._old_reproductionValue = reproductionValue
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
            old_x = self.x
            old_y = self.y
            self.x = neighbour[0][0]
            self.y = neighbour[0][1]
            self._map.updatePixel(self.x, self.y, self.color)
            if checkForReproduction == 'reproduction':
                # mutation = self.getMutation(
                #     self._strength, self._old_reproductionValue)
                mutation = [self._strength, self._old_reproductionValue]
                return {'age': self._age, 'strength': mutation[0], 'reproductionValue': mutation[1], 'x': self.x, 'y': self.y}
            else:
                self._map.updatePixel(old_x, old_y, [0, 124, 5])
                return None
        else:
            # fight
            return None

    def getRndMutation(self, value):
        rnd_plus_minus = randint(0, 1)
        rnd_amount = randint(0, 10)
        if rnd_plus_minus == 0:
            _value = value + rnd_amount
            if _value > 100:
                return value
            else:
                return _value
        elif rnd_plus_minus == 1:
            _value = value - rnd_amount
            if _value < 0:
                return value
            else:
                return _value

    def getMutation(self, strength, reproduction):
        toReturn = []
        toReturn.append(self.getRndMutation(strength))
        toReturn.append(self.getRndMutation(reproduction))
        return toReturn

    def checkFor(self, check):
        if check == 'age':
            if self._age > self._strength:
                return 'dead'
            self._age += 1
            return None
        elif check == 'reproduction':
            if self._reproductionValue > self.reproductionThreshold:
                self._reproductionValue = self._old_reproductionValue
                return 'reproduction'
            else:
                self._reproductionValue += 1
                return None
        else:
            return None
