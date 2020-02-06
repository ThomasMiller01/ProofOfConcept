map_path = 'map.jpg'

# [name, [b, g, r], population, [y, x]]
colonys = [
    ['white', [255, 255, 255], 100, [500, 400]]
]

# world pixel color
world_pixel = {'water': [3, 0, 168], 'empty': [5, 124, 0]}

days_per_generation = 100

population_upper_limit = 1000

# person attributes
p_age = 0

# different kinds of disease
# 'Name': death rate
d_disease = {'Ebola': 30, 'Pest': 20, 'Grippe': 60, 'SaaaschZilla': 90}
