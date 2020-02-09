from random import randint
from numpy import interp
from settings import *


class disaster:
    def __init__(self, _settings):
        self._settings = _settings

        self.allKinds = n_disaster
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
        self.state = 0

    def update(self):
        return None
