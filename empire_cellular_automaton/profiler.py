import cProfile
import re
import pstats

import setup

settings = {
    'p_strength': [0, 100],
    'p_reproductionValue': [0, 70],
    'p_disease': [0, 10, 0],
    'p_child_disease': [0, 10, 0],
    'p_reproductionThreshold': 115,
    'd_strength': [0, 100],
    'd_rate': [0, 10],
    'd_death': 100,
    'maxGen': 10
}

_setup = setup.setup(settings)

cProfile.run('re.compile(_setup.run())', 'restats', sort='time')
