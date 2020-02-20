import couchdb
import json
import os
import numpy as np
import main


random_values = False
maxGen = 1000
dataset_num = 1

map_path = 'map.jpg'

world_pixel = {'water': [3, 0, 168], 'empty': [5, 124, 0]}
colonies = [
    ['red', [255, 0, 0], 100, [500, 400]],
    ['white', [255, 255, 255], 100, [520, 400]],
    ['black', [0, 0, 0], 100, [520, 420]],
    ['yellow', [255, 255, 0], 100, [500, 420]]
]


def numpy_converter(o):
    if isinstance(o, np.int32):
        return int(o)


def getRandInt(low, high):
    return np.random.randint(low, high)


def getRandIntXLessThanY(low, high):
    while True:
        x = np.random.randint(low, high)
        y = np.random.randint(low, high)
        if x < y:
            return [x, y]


def getRandIntBiggerThanY(low, high, y):
    while True:
        x = np.random.randint(low, high)
        if x > y:
            return x


for i in range(dataset_num):
    if random_values:
        reproduction_value = getRandIntXLessThanY(0, 100)
        settings = {
            'p_strength': getRandIntXLessThanY(0, 100),
            'p_reproductionValue': reproduction_value,
            'p_reproductionThreshold': getRandIntBiggerThanY(0, 100, reproduction_value[1]),
            'maxGen': maxGen,
            'colonies': colonies,
            'world_pixel': world_pixel,
            'days_per_generation': 100,
            'map_path': map_path
        }
    else:
        settings = {
            'p_strength': [0, 100],
            'p_reproductionValue': [0, 70],
            'p_reproductionThreshold': 50,
            'maxGen': maxGen,
            'colonies': colonies,
            'world_pixel': world_pixel,
            'days_per_generation': 100,
            'map_path': map_path
        }

    print('-----------')
    print('[' + str(i) + ']')
    print("settings:")
    print(settings)

    # init simulation
    _setup = main.setup(settings)

    # run simulation
    data = _setup.run()

    try:
        os.mkdir("datasets/dataset_" + str(i))
    except:
        pass

    print('saving dataset_' + str(i) + ' ...')
    with open("datasets/dataset_" + str(i) + "/dataset_" + str(i) + "_settings.json", "w") as f:
        json.dump(json.loads(json.dumps(
            settings, default=lambda o: o.__dict__)), f)
    np.save("datasets/dataset_" + str(i) +
            "/dataset_" + str(i) + "_data.npy", data)
    print('[' + str(i) + '] saved')
    print('-----------')

print("all datasets saved")
