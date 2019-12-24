import asyncio
import world_map
import colony
from settings import *
import pygame
import sys


class setup:
    def __init__(self):
        self._colonies = []

        # get object of Map class
        self._map = world_map.Map(map_path, colonys)

        # foreach colony in colonys
        # create new Colony and append to self._colonies
        for i in range(0, colonys.__len__()):
            self._colonies.append(colony.Colony(
                i, colonys[i][0], colonys[i][2], colonys[i][1], colonys[i][3][0], colonys[i][3][1], self._map))

        self.percentages = []

        self.stats = {
            'gen': 0,
            'colonies': self._colonies,
            'percentage': self.percentages
        }

        # set loop
        loop = asyncio.get_event_loop()

        # get starting percentage
        for _colony in self._colonies:
            self.percentages.append(
                [_colony.name, self._map.getColorPercentage(_colony.color)])
        i = 0
        self._map.updateMap()
        # while simulation is running
        while not self.isDone(self.percentages):
            self.stats['gen'] = i
            # init main task
            loop.run_until_complete(self.main(i))
            # clear percentage and append new percentage
            self.percentages.clear()
            for _colony in self._colonies:
                self.percentages.append(
                    [_colony.name, self._map.getColorPercentage(_colony.color)])
            # increase generation count
            i += 1
        # close loop
        loop.close()

        # update map
        self._map.updateMap()

        # quit the program.
        pygame.quit()
        sys.exit(0)

    # task for doing one generation with count=years

    async def renderGeneration(self, _c, count, generation):
        for i in range(0, count):
            _c.update(generation)
            # update map
            self._map.updateMap()
            self._map.updateStats(self.stats)

            # pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit(0)

    # create task for each colony

    async def main(self, generation):
        for _colony in self._colonies:
            asyncio.ensure_future(self.renderGeneration(
                _colony, days_per_generation, generation))

    # check if simulation is done

    def isDone(self, percentage):
        _percentage = False
        # if percentage of one colony is greater than ending_percentage, simulation is done
        for p in percentage:
            if p[1] >= ending_percentage:
                _percentage = True
        _c = []
        # if population of each colony is 0, simulation is done
        for _colony in self._colonies:
            if _colony.population == 0:
                _c.append([_colony.name, False])
        if _c.__len__() == colonys.__len__() or _percentage:
            return True
        return False


if __name__ == "__main__":
    setup()
