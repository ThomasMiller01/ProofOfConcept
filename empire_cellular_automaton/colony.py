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

        _x = self.x
        _y = self.y

        for i in range(0, self.population):
            age = randint(0, 100)
            strength = randint(0, 100)
            reproductionValue = randint(0, 500)
            for j in range(0, 10):
                pixel = self._map.getRandomNeighbour([_x, _y])
                if self._map.getPixelState(pixel) == 'empty':
                    self.people.append(person.Person(
                        i, self._id, self.name, age, strength, reproductionValue, pixel[0][0], pixel[0][1], self.color, self._map))
                    self._map.updatePixel(pixel[0][0], pixel[0][1], self.color)
                    _x = pixel[0][0]
                    _y = pixel[0][1]
                    break

    def update(self):
        for _person in self.people:
            move = _person.move()
            if move == 'dead':
                self.people.remove(_person)
            elif move != None:
                _id = self.people[self.people.__len__() - 1]._id + 1
                self.people.append(person.Person(_id, self._id, self.name,
                                                 move['age'], move['strength'], move['reproductionValue'], move['x'], move['y'], self.color, self._map))
                self.population += 1
                self._map.updatePixel(move['x'], move['y'], self.color)
