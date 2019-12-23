# import what config you want to use
# each config contains image_path and colonies
from config1 import *

days_per_generation = 100

# percentage in %
ending_percentage = 15

# person attributes
p_age = 0

# randint(p_strength[0], p_strength[1])
p_strength = [0, 100]

# randint(p_reproductionValue[0], p_reproductionValue[1])
p_reproductionValue = [0, 100]

# randint(p_disease[0], p_disease[1]) == p_disease[2]
p_disease = [0, 1, 0]

p_reproductionThreshold = 100

# different kinds of disease
# 'Name': death rate
d_disease = {'Ebola': 30, 'Pest': 20, 'Grippe': 60, 'SaaaschZilla': 90}

# randint(d_strength[0], d_strength[1])
d_strength = [0, 100]

# how much increases the disease per round
# randint(d_rate[0], d_rate[1])
d_rate = [0, 10]

# at what value does the person die
d_death = 100
