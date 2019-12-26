import asyncio
import world_map
import colony
from settings import *
import pygame
import sys


class setup:
    def run(self, _settings):
        self._settings = _settings

        self._colonies = []

        # get object of Map class
        self._map = world_map.Map(map_path, colonys)

        # foreach colony in colonys
        # create new Colony and append to self._colonies
        for i in range(0, colonys.__len__()):
            self._colonies.append(colony.Colony(
                i, colonys[i][0], colonys[i][2], colonys[i][1], colonys[i][3][0], colonys[i][3][1], self._map, self._settings))

        self.stats = []

        i = 0

        # while simulation is running
        while not self.isDone():
            self.stats.append({
                'gen': i,
                'data': []
            })
            # init main task
            self.main(i)
            # increase generation count
            i += 1

        return self.stats

    # create task for each colony

    def main(self, generation):
        for _colony in self._colonies:
            self.renderGeneration(_colony, days_per_generation, generation)

    # task for doing one generation with count=years

    def renderGeneration(self, _c, count, generation):
        for i in range(0, count):
            _c.update(generation)
            # update stats here
            if [x for x in self.stats[generation]['data'] if x['day'] == i]:
                self.stats[generation]['data'][i]['colonies'][_c._id] = {
                    'people': _c.people}
            else:
                self.stats[generation]['data'].append({
                    'day': i,
                    'colonies': {
                        _c._id: {
                            'people': _c.people
                        }
                    }
                })

    # check if simulation is done

    def isDone(self):
        if not self.stats:
            return False
        elif self.stats[len(self.stats) - 1]['gen'] == self._settings['maxGen']:
            return True
        else:
            return False
