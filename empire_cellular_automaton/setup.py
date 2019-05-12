import cv2

import world_map
import colony


colonys = [
    ['red', [255, 0, 0], 50, [100, 100]],
    ['green', [0, 255, 0], 50, [200, 200]],
    ['blue', [0, 0, 255], 50, [300, 300]]
]
_colonys = []

_map = world_map.Map('empire_cellular_automaton/map.jpg', colonys)

for i in range(0, colonys.__len__()):
    _colonys.append(colony.Colony(
        i, colonys[i][0], colonys[i][2], colonys[i][1], colonys[i][3][0], colonys[i][3][1], _map))

cv2.waitKey(0)
cv2.destroyAllWindows()
