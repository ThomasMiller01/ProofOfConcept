from random import randint
import random


class Person:
    def __init__(self, _id, colonyID, colonyName, age, strength, reproductionValue, x, y, color, _map):
        # set person attributes
        self._id = _id
        self._colonyID = colonyID
        self._colonyName = colonyName
        self._age = age
        self._strength = strength
        self._reproductionValue = reproductionValue
        self._old_reproductionValue = reproductionValue
        self.reproductionThreshold = 118
        self.x = x
        self.y = y
        self.color = color
        self._map = _map

    def move(self):
        # get rnd place around person
        neighbour = self._map.getRandomNeighbour([self.x, self.y])
        # check if rnd place is water, empty, etc.
        neighbour_state = self._map.getPixelState(neighbour)
        # check if person needs to die / reproduce, increase age and reproduction_value
        checkForAge = self.checkFor('age')
        checkForReproduction = self.checkFor('reproduction')
        # if person needs to die, return checkForAge
        if checkForAge != None:
            return checkForAge
        # check what state the rnd place is
        if neighbour_state == 'water':
            # if person wants to move to water, do nothing
            return None
        elif neighbour_state == 'empty' or neighbour_state == self._colonyName:
            # person wants to move to an empty place
            # get old x and y values
            old_x = self.x
            old_y = self.y
            # set new x and y values from empty place
            self.x = neighbour[0][0]
            self.y = neighbour[0][1]
            # update pixel of new place
            self._map.updatePixel(self.x, self.y, self.color)
            # if person needs to reproduce
            if checkForReproduction == 'reproduction':
                # get mutation for strength and reproduction_value
                mutation_strength = self.getMutation(self._strength)
                mutation_reproductionsValue = self.getMutation(
                    self._old_reproductionValue)
                # return data, child person gets
                return {'age': self._age, 'strength': mutation_strength, 'reproductionValue': mutation_reproductionsValue, 'x': self.x, 'y': self.y}
            else:
                # if person only moves, set old place to empty place color
                self._map.updatePixel(old_x, old_y, [0, 124, 5])
                return None
        else:
            # person fights other colony
            return None

    def getMutation(self, value):
        # get rnd +/- and rnd value [0;10]
        rnd_plus_minus = randint(0, 1)
        rnd_amount = randint(0, 10)
        if rnd_plus_minus == 0:
            _value = value + rnd_amount
            # if rnd value is bigger than 100 return old value
            if _value > 100:
                return value
            else:
                # else return new value
                return _value
        elif rnd_plus_minus == 1:
            _value = value - rnd_amount
            # if rnd value is less than 0 return old value
            if _value < 0:
                return value
            else:
                # else return new value
                return _value

    def checkFor(self, check):
        if check == 'age':
            # if age is bigger than strength, person needs to die
            if self._age > self._strength:
                return 'dead'
            self._age += 1
            return None
        elif check == 'reproduction':
            # if reproduction_value is bihher than reproduction_threshold, person needs to reproduce
            if self._reproductionValue > self.reproductionThreshold:
                self._reproductionValue = self._old_reproductionValue
                return 'reproduction'
            else:
                # else increase reproduction_value
                self._reproductionValue += 1
                return None
        else:
            return None
