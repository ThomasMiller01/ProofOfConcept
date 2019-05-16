import cv2
import asyncio

import world_map
import colony

# [name, [r, g, b], population, [x, y]]
colonys = [
    ['red', [0, 0, 255], 100, [675, 213]],
    ['yellow', [0, 255, 255], 100, [506, 443]],
    ['white', [255, 255, 255], 100, [138, 219]]
]
_colonys = []

_map = world_map.Map(
    'map.jpg', colonys)

for i in range(0, colonys.__len__()):
    _colonys.append(colony.Colony(
        i, colonys[i][0], colonys[i][2], colonys[i][1], colonys[i][3][0], colonys[i][3][1], _map))


async def myTask(_c, count):
    print("Rendering Colony: '" + _c.name + "'")
    for i in range(0, count):
        _c.update()
    print("Population: " + str(_c.population))
    print("---------------------")


async def main():
    for _colony in _colonys:
        asyncio.ensure_future(myTask(_colony, 100))


def isDone(percentage):
    _percentage = False
    for p in percentage:
        if p[1] >= 15:
            _percentage = True
    _c = []
    for _colony in _colonys:
        if _colony.population == 0:
            _c.append([_colony.name, False])
    if _c.__len__() == colonys.__len__() or _percentage:
        return True
    return False


loop = asyncio.get_event_loop()
percentages = []
for _colony in _colonys:
    percentages.append([_colony.name, _map.getColorPercentage(_colony.color)])
i = 0
while not isDone(percentages):
    # cv2.waitKey(0)
    print("---------------------")
    print("Generation: " + str(i + 1))
    print("---------------------")
    loop.run_until_complete(main())
    print("---------------------")
    print("Rendered all colonys")
    print("---------------------")
    percentages.clear()
    for _colony in _colonys:
        percentages.append(
            [_colony.name, _map.getColorPercentage(_colony.color)])
    print("---------------------")
    print("Percentage:")
    print(percentages)
    print("---------------------")
    i += 1
    _map.updateMap()
loop.close()

_map.updateMap()

cv2.waitKey(0)
cv2.destroyAllWindows()
