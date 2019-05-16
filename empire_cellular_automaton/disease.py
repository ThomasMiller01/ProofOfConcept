from random import randint


class disease:
    def __init__(self, kind, strength):
        self.allKindes = {'Ebola': 70, 'Pest': 80, 'Grippe': 50}

        self.kind = [kind, self.allKindes[kind]]
        self.strength = strength
        self.state = 0

    def getDeathRate(self):
        return self.kind[1]

    def update(self):
        _rnd = randint(0, 10)
        if _rnd == 1:
            return False
        if self.state >= 100:
            return False
        else:
            rnd = randint(0, 10) * 0.1
            self.state += rnd
            return True
