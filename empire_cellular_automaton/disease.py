from random import randint
from numpy import interp


class disease:
    def __init__(self):
        self.allKinds = {'Ebola': 70, 'Pest': 80,
                         'Grippe': 40, 'SaaaschZilla': 10}
        chances_Nmb = 0
        for _kind in self.allKinds:
            chances_Nmb += 100 - self.allKinds[_kind]
        rndInt = randint(0, chances_Nmb)
        lowValue = 0
        self.kind = None
        for chance in self.allKinds:
            if rndInt >= lowValue and rndInt <= lowValue + (100 - self.allKinds[chance]):
                self.kind = [chance, self.allKinds[chance]]
                break
            lowValue += 100 - self.allKinds[chance]
        self.strength = randint(0, 100)
        self.state = 0

    def getDeathRate(self):
        return self.kind[1]

    def update(self):
        # _rnd = randint(0, 100)
        # if _rnd == 0:
        #     return False
        if self.state >= 100:
            return False
        else:
            rnd = randint(0, 10) * 0.1
            self.state += rnd
            return True
