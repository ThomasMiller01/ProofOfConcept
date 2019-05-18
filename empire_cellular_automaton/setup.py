import asyncio
import pygame

import world_map
import colony

# [name, [r, g, b], population, [x, y]]
colonys = [
    ['red', [255, 0, 0], 100, [675, 213]],
    ['yellow', [255, 255, 0], 100, [506, 443]],
    ['white', [255, 255, 255], 100, [138, 219]]
]
_colonys = []

# get object of Map class
_map = world_map.Map(
    'empire_cellular_automaton/map.jpg', colonys)

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
        asyncio.ensure_future(myTask(_colony, 100, generation))


# check if simulation is done
def isDone(percentage):
    _percentage = False
    # if percentage of one colony is greater than 15, simulation is done
    for p in percentage:
        if p[1] >= 15:
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
clock = pygame.time.Clock()
_map.updateMap()
# while simulation is running
while not isDone(percentages):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # quit pygame
            pygame.quit()
            # quit the program.
            quit()
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
    clock.tick(1)
# close loop
loop.close()

# update map
_map.updateMap()

# quit pygame
pygame.quit()

# quit the program.
quit()
