from random import randint


class Person:
    def __init__(self, _id, colonyID, colonyName, age, strength, reproductionValue, x, y, color, _map):
        self._id = _id
        self._colonyID = colonyID
        self._colonyName = colonyName
        self._age = age
        self._strength = strength
        self._reproductionValue = reproductionValue
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
            if checkForReproduction != None:
                return {'age': self._age, 'strength': self._strength, 'reproductionValue': self._reproductionValue, 'x': self.x, 'y': self.y}
            else:
                return None
        else:
            # fight
            return None

    def checkFor(self, check):
        if check == 'age':
            # check if person dies of age
            # return 'dead'
            return None
        elif check == 'reproduction':
            rnd = randint(0, 500)
            if rnd == self._reproductionValue:
                return 'reproduction'
            else:
                return None
        else:
            return None
