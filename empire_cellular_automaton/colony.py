from random import randint

import person


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
            self._map.updatePixel(self.x, self.y, color)

        for i in range(0, self.population):
            age = 0
            strength = randint(0, 100)
            reproductionValue = randint(0, 100)
            pixel = self._map.getPixel(self.x, self.y)
            self.people.append(person.Person(
                i, self._id, self.name, age, strength, reproductionValue, self.x, self.y, self.color, self._map))
            self._map.updatePixel(self.x, self.y, self.color)

    def update(self):
        for _person in self.people:
            move = _person.move()
            if move == 'dead':
                self._map.updatePixel(_person.x, _person.y, [0, 124, 5])
                self.people.remove(_person)
            elif move != None:
                _id = self.people[self.people.__len__() - 1]._id + 1
                self.people.append(person.Person(_id, self._id, self.name,
                                                 move['age'], move['strength'], move['reproductionValue'], move['x'], move['y'], self.color, self._map))
                self._map.updatePixel(move['x'], move['y'], self.color)
        self.population = self.people.__len__()
