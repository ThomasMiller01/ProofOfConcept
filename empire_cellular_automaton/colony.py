from random import randint

import person
import disease
from settings import *


class Colony:
    def __init__(self, _id, name, population, color, x, y, _map, _settings):
        self._id = _id
        self.name = name
        self.population = population
        self.color = color
        self.x = x
        self.y = y
        self._map = _map
        self.people = []

        self._settings = _settings

        # check if the colony start on land
        if self._map.getPixelState([[self.x, self.y], self._map._pixel_arr[self.x, self.y]]) != 'empty':
            # colony would not start on empty land ...
            raise
        else:
            # set startpoint with color
            self._map.updatePixel(self.x, self.y, color)

        # create person in range(0, population_nmb)
        for i in range(0, self.population):
            # init attributes
            age = p_age
            strength = randint(
                self._settings['p_strength'][0], self._settings['p_strength'][1])
            reproductionValue = randint(
                self._settings['p_reproductionValue'][0], self._settings['p_reproductionValue'][1])
            if randint(self._settings['p_disease'][0], self._settings['p_disease'][1]) == self._settings['p_disease'][2]:
                _disease = disease.disease(self._settings)
            else:
                _disease = None
            pixel = self._map._pixel_arr[self.x, self.y]
            self.people.append(person.Person(
                i, self._id, self.name, age, strength, reproductionValue, _disease, self.x, self.y, self.color, self._map, self._settings))
            self._map.updatePixel(self.x, self.y, self.color)

    def update(self, generation):
        # natural disaster
        if generation % 3 == 0:
            # do natural disaster
            pass
        # foreach person
        for _person in self.people:
            # call persons move() function
            move = _person.move(generation, self.people)
            # if person is dead, remove person and change pixel color
            if move == 'dead':
                if _person._setPixelColorBack:
                    self._map.updatePixel(
                        _person.x, _person.y, world_pixel['empty'])
                self.people.remove(_person)
            # if person needs to reproduce, create new person with given attributes
            elif move != None and 'age' in move:
                _id = self.people[self.people.__len__() - 1]._id + 1
                self.people.append(person.Person(_id, self._id, self.name,
                                                 0, move['strength'], move['reproductionValue'], move['disease'], move['x'], move['y'], self.color, self._map, self._settings))
                self._map.updatePixel(move['x'], move['y'], self.color)
        self.population = self.people.__len__()
