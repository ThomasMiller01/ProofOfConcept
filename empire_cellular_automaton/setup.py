import asyncio
import pygame
import multiprocessing as mp
import world_map
import colony


def main(generation):
    print('---------------------')
    print('Rendering ...')
    print('---------------------')
    pool = mp.Pool(mp.cpu_count())

    results = pool.starmap(
        myTask, [(_colony, 100, generation) for _colony in _colonys])
    print(results)
    print('---------------------')
    for _colony in results:
        print('.....................')
        print('Colony: ' + _colony[0])
        print('Population: ' + str(_colony[1]))
        print('.....................')
    print('---------------------')


# task for doing one generation with count=years
def myTask(_c, count, generation):
    for i in range(0, count):
        _c.update(generation)
    return [_c.name, _c.population]


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


if __name__ == "__main__":

    # [name, [r, g, b], population, [x, y]]
    colonys = [
        ['red', [255, 0, 0], 100, [675, 213]],
        ['yellow', [255, 255, 0], 100, [506, 443]],
        ['white', [255, 255, 255], 100, [138, 219]]
    ]
    _colonys = []

    # get object of Map class and Map_Utilities class
    _map = world_map.Map(
        'empire_cellular_automaton/map.jpg', colonys)
    _map_utilities = _map.map_utilities

    # foreach colony in colonys
    # create new Colony and append to _colonys
    for i in range(0, colonys.__len__()):
        _colonys.append(colony.Colony(
            i, colonys[i][0], colonys[i][2], colonys[i][1], colonys[i][3][0], colonys[i][3][1], _map_utilities))

    percentages = []
    # get starting percentage
    for _colony in _colonys:
        percentages.append(
            [_colony.name, _map.getColorPercentage(_colony.color)])
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
        main(i)
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
        clock.tick(1000)
    # close loop

    # update map
    _map.updateMap()

    # quit pygame
    pygame.quit()

    # quit the program.
    quit()
