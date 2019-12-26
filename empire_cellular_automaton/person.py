from random import randint
import random
from numpy import interp
import disease
from settings import *


class Person:
    def __init__(self, _id, colonyID, colonyName, age, strength, reproductionValue, disease, x, y, color, _map):
        # set person attributes
        self._id = _id
        self._colonyID = colonyID
        self._colonyName = colonyName
        self._age = age
        self._strength = strength
        self._reproductionValue = reproductionValue
        self._old_reproductionValue = reproductionValue
        self.reproductionThreshold = p_reproductionThreshold
        self._disease = disease
        self.x = x
        self.y = y
        self.color = color
        self._map = _map
        # set pixel color back to empty if person moves or dies
        self._setPixelColorBack = True

    def move(self, generation):
        # check if person needs to die / reproduce, increase age and reproduction_value
        checkForAge = self.checkFor('age')
        checkForReproduction = self.checkFor('reproduction')
        checkForDisease = self.checkFor('disease')
        checkForOwnTerritory = self.checkFor('ownTerritory')
        # checkForAge = None
        # checkForReproduction = None
        # checkForDisease = None
        # checkForOwnTerritory = None
        # if person needs to die, return 'dead'
        if checkForAge == 'dead':
            return checkForAge
        if checkForOwnTerritory == None:
            # get rnd place around person
            neighbour = self._map.getRandomNeighbour([self.x, self.y])
            # check if rnd place is water, empty, etc.
            neighbour_state = self._map.getPixelState(neighbour)
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
                    if self._disease != None:
                        rndNmb = randint(0, 1)
                        if rndNmb == 0:
                            _disease = self._disease
                            _disease.state = 0
                        else:
                            rndNmb = randint(0, 10)
                            if rndNmb == 0:
                                _disease = disease.disease()
                            else:
                                _disease = None

                    else:
                        rndNmb = randint(
                            p_child_disease[0], p_child_disease[1])
                        if rndNmb == p_child_disease[2]:
                            _disease = disease.disease()
                        else:
                            _disease = None
                    # return data, child person gets
                    return {'age': self._age, 'strength': mutation_strength, 'reproductionValue': mutation_reproductionsValue, 'disease': _disease, 'x': old_x, 'y': old_y}
                else:
                    # if person only moves, set old place to empty place color
                    if self._setPixelColorBack:
                        # todo do it only if no other person from colony is on the place
                        self._map.updatePixel(
                            old_x, old_y, world_pixel['empty'])
                    return None
            else:
                # person fights other colony
                return None
        else:
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
        else:
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
            # if reproduction_value is bigger than reproduction_threshold, person needs to reproduce
            if self._reproductionValue > self.reproductionThreshold:
                self._reproductionValue = self._old_reproductionValue
                return 'reproduction'
            else:
                # else increase reproduction_value
                self._reproductionValue += 1
                return None
        elif check == 'disease':
            # if person has disease
            if self._disease != None:
                # if person still has disease
                if self._disease.update():
                    # get deathrate
                    deathRate = self._disease.getDeathRate() * 0.1
                    rndNmb = randint(0, 100)
                    if rndNmb < deathRate:
                        return 'dead'
                    rate = self._disease.state * self._disease.strength * self._disease.getDeathRate()
                    _mapped = interp(rate, [0, 10000], [0, 1])
                    # map death rate between 0 and 1
                    self._age *= 1 + _mapped
                    return None
                else:
                    return None
            else:
                # person can get a disease here
                return None
        # check if person is surrounded by its own territory
        # if true delete person
        elif check == 'ownTerritory':
            xy = []
            # oben
            xy.append([self.x, self.y + 1])
            # oben rechts
            xy.append([self.x + 1, self.y + 1])
            # rechts
            xy.append([self.x + 1, self.y])
            # unten rechts
            xy.append([self.x + 1, self.y - 1])
            # unten
            xy.append([self.x, self.y - 1])
            # unten links
            xy.append([self.x - 1, self.y - 1])
            # links
            xy.append([self.x - 1, self.y])
            # oben links
            xy.append([self.x - 1, self.y + 1])
            for _xy in xy:
                if self._map.getPixelState([[], self._map._pixel_arr[_xy[0], _xy[1]]]) != self._colonyName:
                    return None
            rnd = randint(0, 40)
            if rnd == 0:
                # return None
                return 'ownTerritory'
            else:
                return None
        else:
            return None
