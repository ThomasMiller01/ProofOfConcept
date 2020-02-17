import cProfile
import re
import pstats

import main

settings = {
    'p_strength': [0, 100],
    'p_reproductionValue': [0, 70],
    'p_reproductionThreshold': 40,
    'maxGen': 5
}

_setup = main.setup(settings)

cProfile.run('re.compile(_setup.run())', 'restats', sort='time')
