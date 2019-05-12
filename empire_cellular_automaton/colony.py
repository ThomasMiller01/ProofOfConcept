from random import randint

import person


class Colony:
    def __init__(self, _id, name, population_nmb, color, x, y, _map):
        self._id = _id
        self.name = name
        self.population_nmb = population_nmb
        self.color = color
        self.x = x
        self.y = y
        self._map = map
        self.people = []

        for i in range(0, population_nmb):
            age = randint(0, 100)
            strength = randint(0, 100)
            reproductionValue = randint(0, 10)
            self.people.append(person.Person(
                i, self._id, age, strength, reproductionValue))
