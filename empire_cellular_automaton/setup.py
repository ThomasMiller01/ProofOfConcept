import asyncio
import world_map
import colony
from settings import *
import pygame
import sys
import copy
import person
import time


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

        if display_map:
            self._stats = {
                'gen': 0,
                'day': 0,
                'colonies': self._colonies
            }

        i = 0

        self._map.updateMap()

        start_time = time.time()

        # while simulation is running
        while not self.isDone():
            self.stats.append({
                'gen': i,
                'data': []
            })
            if display_map:
                self._stats['gen'] = i
            print("gen " + str(i) + " started calculating ..")
            gen_start_time = time.time()
            # init main task
            self.main(i)
            gen_end_time = time.time()
            print("gen " + str(i) + " rendered in " +
                  str(round(gen_end_time - gen_start_time, 4)) + "s")
            print("******")
            # increase generation count
            i += 1

        end_time = time.time()

        print("- finished calculating ...")
        print("- time elapsed: " + str(round(end_time - start_time, 4)) + "s")

        if display_map:
            pygame.quit()

        return self.stats

    # create task for each colony

    def main(self, generation):
        for _colony in self._colonies:
            self.renderGeneration(_colony, days_per_generation, generation)

    # task for doing one generation with count=years

    def renderGeneration(self, _c, count, generation):
        for i in range(0, count):
            _c.update(generation)

            if display_map:
                self._stats['day'] = i
                self._map.updateMap()
                self._map.updateStats(self._stats)

                # pygame events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit(0)

            # update stats here
            if [x for x in self.stats[generation]['data'] if x['day'] == i]:
                self.stats[generation]['data'][i]['colonies'][_c._id] = {
                    'people': [copy.deepcopy(person.Person(x._id, x._colonyID, x._colonyName, x._age, x._strength, x._reproductionValue, x._disease, x.x, x.y, x.color, None, x._settings)) for x in _c.people]}
            else:
                self.stats[generation]['data'].append({
                    'day': i,
                    'colonies': {
                        _c._id: {
                            'people': [copy.deepcopy(person.Person(x._id, x._colonyID, x._colonyName, x._age, x._strength, x._reproductionValue, x._disease, x.x, x.y, x.color, None, x._settings)) for x in _c.people]
                        }
                    }
                })

    # check if simulation is done

    def isDone(self):
        if not self.stats:
            return False
        elif self.stats[len(self.stats) - 1]['gen'] + 1 == self._settings['maxGen']:
            return True
        else:
            return False
