from random import randint


class disease:
    def __init__(self, kind, strength):
        self.allKindes = {'Ebola': 70, 'Pest': 90, 'Grippe': 20}

        self.kind = self.allKindes[kind]
        self.strength = strength
        self.state = 0

    def getDeathRate(self):
        return self.kind[1]

    def update(self):
        if self.state >= 100:
            return False
        else:
            rnd = randint(0, 10) * 0.1
            self.state += rnd
            return True
