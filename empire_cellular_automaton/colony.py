from random import randint

import person
import disease


class Colony:
    def __init__(self, _id, name, population, color, x, y, _map):
        self._id = _id
        self.name = name
        self.population = population
        self.color = color
        self.x = x
        self.y = y
        self._map = _map
        self.people = []

        # check if the colony start on land
        if self._map.getPixelState([[self.x, self.y], self._map.getPixel(self.x, self.y)]) != 'empty':
            # colony would not start on empty land ...
            raise
        else:
            # set startpoint with color
            self._map.updatePixel(self.x, self.y, color)

        # create person in range(0, population_nmb)
        for i in range(0, self.population):
            # init attributes
            age = 0
            strength = randint(0, 100)
            reproductionValue = randint(0, 100)
            pixel = self._map.getPixel(self.x, self.y)
            self.people.append(person.Person(
                i, self._id, self.name, age, strength, reproductionValue, None, self.x, self.y, self.color, self._map))
            self._map.updatePixel(self.x, self.y, self.color)

    def update(self):
        # foreach person
        for _person in self.people:
            # call persons move() function
            move = _person.move()
            # if person is dead, remove person and change pixel color
            if move == 'dead':
                # self._map.updatePixel(_person.x, _person.y, [0, 124, 5])
                self.people.remove(_person)
            # if person needs to reproduce, create new person with given attributes
            elif move != None:
                _id = self.people[self.people.__len__() - 1]._id + 1
                self.people.append(person.Person(_id, self._id, self.name,
                                                 0, move['strength'], move['reproductionValue'], None, move['x'], move['y'], self.color, self._map))
                self._map.updatePixel(move['x'], move['y'], self.color)
        self.population = self.people.__len__()