import couchdb
import json
import os
import numpy as np
import main


random_values = False
maxGen = 1000
dataset_num = 1


# server = couchdb.Server('http://localhost:5984/')
# db = server['dataset_test_1']


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
            'maxGen': maxGen
        }
    else:
        settings = {
            'p_strength': [0, 100],
            'p_reproductionValue': [0, 70],
            'p_reproductionThreshold': 40,
            'maxGen': maxGen
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
