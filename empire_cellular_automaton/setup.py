import asyncio
import world_map
import colony
from settings import *

_colonys = []

# get object of Map class
_map = world_map.Map(map_path, colonys)

# foreach colony in colonys
# create new Colony and append to _colonys
for i in range(0, colonys.__len__()):
    _colonys.append(colony.Colony(
        i, colonys[i][0], colonys[i][2], colonys[i][1], colonys[i][3][0], colonys[i][3][1], _map))

percentages = []

# calculate percentages for stats
for _colony in _colonys:
    percentages.append(
        [_colony.name, _map.getColorPercentage(_colony.color)])

stats = {
    'gen': 0,
    'colonies': _colonys,
    'percentage': percentages
}

# task for doing one generation with count=years


async def renderGeneration(_c, count, generation):
    for i in range(0, count):
        _c.update(generation)
        # update map
        _map.updateMap()
        _map.updateStats(stats)
    print("Rendered Colony: '" + _c.name + "'")
    print("Population: " + str(_c.population))
    print("---------------------")


# create task for each colony
async def main(generation):
    for _colony in _colonys:
        asyncio.ensure_future(renderGeneration(
            _colony, days_per_generation, generation))


# check if simulation is done
def isDone(percentage):
    _percentage = False
    # if percentage of one colony is greater than ending_percentage, simulation is done
    for p in percentage:
        if p[1] >= ending_percentage:
            _percentage = True
    _c = []
    # if population of each colony is 0, simulation is done
    for _colony in _colonys:
        if _colony.population == 0:
            _c.append([_colony.name, False])
    if _c.__len__() == colonys.__len__() or _percentage:
        return True
    return False


# set loop
loop = asyncio.get_event_loop()

# get starting percentage
for _colony in _colonys:
    percentages.append([_colony.name, _map.getColorPercentage(_colony.color)])
i = 0
_map.updateMap()
# while simulation is running
while not isDone(percentages):
    stats['gen'] = i
    print("---------------------")
    print("Generation: " + str(i + 1))
    print("---------------------")
    # init main task
    loop.run_until_complete(main(i))
    print("---------------------")
    print("Rendered all colonys")
    print("---------------------")
    # clear percentage and append new percentage
    percentages.clear()
    for _colony in _colonys:
        percentages.append(
            [_colony.name, _map.getColorPercentage(_colony.color)])
    print("---------------------")
    print("Percentage:")
    print(percentages)
    print("---------------------")
    # increase generation count
    i += 1
# close loop
loop.close()

# update map
_map.updateMap()

# quit the program.
quit()
