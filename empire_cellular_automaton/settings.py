# path to the map image
map_path = 'map.jpg'

# [name, [b, g, r], population, [y, x]]
colonys = [
    ['red', [0, 0, 255], 100, [464, 327]],
    ['yellow', [0, 255, 255], 100, [139, 221]],
    ['white', [255, 255, 255], 1000, [659, 201]]
]

# world pixel color
world_pixel = {'water': [168, 0, 3], 'empty': [0, 124, 5]}

days_per_generation = 100

# percentage in %
ending_percentage = 15

# time between different frames
# 0 = wait for key
wait_time = 1000

# person attributes
p_age = 0

# randint(p_strength[0], p_strength[1])
p_strength = [0, 100]

# randint(p_reproductionValue[0], p_reproductionValue[1])
p_reproductionValue = [0, 100]

# randint(p_disease[0], p_disease[1]) == p_disease[2]
p_disease = [0, 1, 0]

p_reproductionThreshold = 118

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
