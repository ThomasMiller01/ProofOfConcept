from random import randint
from numpy import interp
from settings import *


class disease:
    def __init__(self, _settings):
        self._settings = _settings

        self.allKinds = d_disease
        chances_Nmb = 0
        for _kind in self.allKinds:
            chances_Nmb += self.allKinds[_kind][0]
        rndInt = randint(0, chances_Nmb)
        lowValue = 0
        self.kind = None
        for chance in self.allKinds:
            if rndInt >= lowValue and rndInt <= lowValue + (100 - self.allKinds[chance][0]):
                self.kind = [chance, self.allKinds[chance]]
                break
            lowValue += 100 - self.allKinds[chance][0]
        self.strength = randint(
            self._settings['d_strength'][0], self._settings['d_strength'][1])
        self.state = 0

    def getDeathRate(self):
        return self.kind[1][0]

    def update(self):
        if self.state >= self._settings['d_death'] or self.kind[1][1] < randint(0, 100):
            return False
        else:
            rnd = randint(self._settings['d_rate']
                          [0], self._settings['d_rate'][1]) * 0.1
            self.state += rnd
            return True
