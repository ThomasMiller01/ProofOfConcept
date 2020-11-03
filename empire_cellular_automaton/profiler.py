import cProfile
import re
import pstats

import main

display_map = True

map_path = 'map.jpg'

world_pixel = {'water': [3, 0, 168], 'empty': [5, 124, 0]}
colonies = [
    ['white', [255, 255, 255], 100, [520, 400]]
]

settings = {
    'p_strength': [0, 100],
    'p_reproductionValue': [0, 70],
    'p_reproductionThreshold': 50,
    'maxGen': 10,
    'display_map': display_map,
    'colonies': colonies,
    'world_pixel': world_pixel,
    'days_per_generation': 100,
    'map_path': map_path
}

_setup = main.setup(settings)

cProfile.run('re.compile(_setup.run())', 'restats', sort='time')
