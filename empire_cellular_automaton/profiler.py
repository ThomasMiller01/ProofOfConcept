import cProfile
import re
import pstats

import setup

cProfile.run('re.compile(setup.setup())', 'restats', sort='time')
