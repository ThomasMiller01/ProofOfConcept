from random import randint
from numpy import interp
from settings import *


class disease:
    def __init__(self):
        self.allKinds = d_disease
        chances_Nmb = 0
        for _kind in self.allKinds:
            chances_Nmb += self.allKinds[_kind]
        rndInt = randint(0, chances_Nmb)
        lowValue = 0
        self.kind = None
        for chance in self.allKinds:
            if rndInt >= lowValue and rndInt <= lowValue + (self.allKinds[chance]):
                self.kind = [chance, self.allKinds[chance]]
                break
            lowValue += self.allKinds[chance]
        self.strength = randint(d_strength[0], d_strength[1])
        self.state = 0

    def getDeathRate(self):
        return self.kind[1]

    def update(self):
        if self.state >= d_death:
            return False
        else:
            rnd = randint(d_rate[0], d_rate[1]) * 0.1
            self.state += rnd
            return True
