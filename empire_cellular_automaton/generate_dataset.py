import couchdb
import json
from random import randint
import os
import numpy as np
import setup


random_values = False
maxGen = 10
dataset_num = 1


# server = couchdb.Server('http://localhost:5984/')
# db = server['dataset_test_1']


def numpy_converter(o):
    if isinstance(o, np.int32):
        return int(o)


def getRandIntXLessThanY(low, high):
    while True:
        x = randint(low, high)
        y = randint(low, high)
        if x < y:
            return [x, y]


def getRandIntXLessThanYAndZNotBiggerThanY(low, high):
    while True:
        x = randint(low, high)
        y = randint(low, high)
        z = randint(low, high)
        if x < y and z < y and z > x:
            return [x, y, z]


def getRandIntBiggerThanY(low, high, y):
    while True:
        x = randint(low, high)
        if x > y:
            return x


for i in range(dataset_num):
    if random_values:
        reproduction_value = getRandIntXLessThanY(0, 100)
        settings = {
            'p_strength': getRandIntXLessThanY(0, 100),
            'p_reproductionValue': reproduction_value,
            'p_disease': getRandIntXLessThanYAndZNotBiggerThanY(0, 100),
            'p_child_disease': getRandIntXLessThanYAndZNotBiggerThanY(0, 100),
            'p_reproductionThreshold': getRandIntBiggerThanY(0, 100, reproduction_value[1]),
            'd_strength': getRandIntXLessThanY(0, 100),
            'd_rate': getRandIntXLessThanY(0, 100),
            'd_death': randint(0, 100),
            'maxGen': maxGen
        }
    else:
        settings = {
            'p_strength': [0, 100],
            'p_reproductionValue': [0, 70],
            'p_disease': [0, 10, 0],
            'p_child_disease': [0, 10, 0],
            'p_reproductionThreshold': 50,
            'd_strength': [0, 100],
            'd_rate': [0, 10],
            'd_death': 100,
            'maxGen': maxGen
        }

    print('-----------')
    print('[' + str(i) + ']')
    print("settings:")
    print(settings)

    # init simulation
    _setup = setup.setup(settings)

    # run simulation
    data = _setup.run()

    try:
        os.mkdir("datasets/dataset_" + str(i))
    except:
        pass

    serialized_data = json.dumps(settings, default=lambda o: o.__dict__)
    # db.save(json.loads(serialized_data))
    print('saving dataset_' + str(i) + ' ...')
    with open("datasets/dataset_" + str(i) + "/dataset_" + str(i) + "_settings.json", "w") as f:
        json.dump(json.loads(serialized_data), f)
    np.save("datasets/dataset_" + str(i) +
            "/dataset_" + str(i) + "_data.npy", data)
    print('[' + str(i) + '] saved')
    print('-----------')

print("all datasets saved")
