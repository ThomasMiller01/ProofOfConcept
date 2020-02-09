from enum import Enum

map_path = 'map.jpg'

# [name, [b, g, r], population, [y, x]]
colonys = [
    ['white', [255, 255, 255], 100, [500, 400]]
]

# world pixel color
world_pixel = {'water': [3, 0, 168], 'empty': [5, 124, 0]}

days_per_generation = 100

population_upper_limit = 200

display_map = True

# person attributes
p_age = 0

# different kinds of disease
# 'Name': death rate
d_disease = {'Ebola': [30, 15], 'Pest': [20, 20], 'Grippe': [
    60, 50], 'SaaaschZilla': [90, 5], 'CoronaVirus': [10, 70]}

n_disaster = {'Tsunami': 30, 'Meteor': 70,
              'Vulcano': 20, 'Earthquake': 30, 'Hurican': 15}


class PersonMoveIn(Enum):
    age = 'age'
    reproduction = 'reproduction'
    disease = 'disease'
    ownTerritory = 'ownterritory'


class PersonMoveOut(Enum):
    null = None
    dead = 'dead'
    reproduction = 'reproduction'
    ownTerritory = 'ownTerritory'
