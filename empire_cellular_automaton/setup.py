import asyncio
import cv2
import world_map
import colony
from settings import *

_colonys = []

# get object of Map class
_map = world_map.Map(map_path, colonys)
# cv2.waitKey(0)

# foreach colony in colonys
# create new Colony and append to _colonys
for i in range(0, colonys.__len__()):
    _colonys.append(colony.Colony(
        i, colonys[i][0], colonys[i][2], colonys[i][1], colonys[i][3][0], colonys[i][3][1], _map))


# task for doing one generation with count=years
async def myTask(_c, count, generation):
    print("Rendering Colony: '" + _c.name + "'")
    for i in range(0, count):
        _c.update(generation)
    print("Population: " + str(_c.population))
    print("---------------------")


# create task for each colony
async def main(generation):
    for _colony in _colonys:
        asyncio.ensure_future(myTask(_colony, days_per_generation, generation))


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
percentages = []
# get starting percentage
for _colony in _colonys:
    percentages.append([_colony.name, _map.getColorPercentage(_colony.color)])
i = 0
_map.updateMap()
# while simulation is running
while not isDone(percentages):
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
    # update map
    _map.updateMap()
    cv2.waitKey(wait_time)
# close loop
loop.close()

# update map
_map.updateMap()

# quit pygame
cv2.destroyAllWindows()

# quit the program.
quit()
