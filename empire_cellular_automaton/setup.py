import cv2

import world_map
import colony

# [name, [r, g, b], population, [x, y]]
colonys = [
    ['red', [0, 0, 255], 100, [675, 213]],
    ['yellow', [0, 255, 255], 100, [506, 443]],
    ['white', [255, 255, 255], 100, [138, 219]]
]
_colonys = []

_map = world_map.Map('empire_cellular_automaton/map.jpg', colonys)

for i in range(0, colonys.__len__()):
    _colonys.append(colony.Colony(
        i, colonys[i][0], colonys[i][2], colonys[i][1], colonys[i][3][0], colonys[i][3][1], _map))

for i in range(0, 500):
    for _colony in _colonys:
        _colony.update()
    # if i % 10 == 0:
    #     _map.updateMap()
    #     cv2.waitKey(0)

_map.updateMap()
_map.getColorPercentage(colonys[0][1])
cv2.waitKey(0)
cv2.destroyAllWindows()
