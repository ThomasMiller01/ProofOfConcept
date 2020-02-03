import json
import setup
import couchdb
from random import randint

# server = couchdb.Server('http://localhost:5984/')

# db = server['dataset_test_1']

maxGen = 3


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


_setup = setup.setup()

for i in range(5):
    settings = {
        'p_strength': [0, 100],
        'p_reproductionValue': [0, 70],
        'p_disease': [0, 10, 0],
        'p_child_disease': [0, 10, 0],
        'p_reproductionThreshold': 115,
        'd_strength': [0, 100],
        'd_rate': [0, 10],
        'd_death': 100,
        'maxGen': 4
    }

    # reproduction_value = getRandIntXLessThanY(0, 100)

    # settings = {
    #     'p_strength': getRandIntXLessThanY(0, 100),
    #     'p_reproductionValue': reproduction_value,
    #     'p_disease': getRandIntXLessThanYAndZNotBiggerThanY(0, 100),
    #     'p_child_disease': getRandIntXLessThanYAndZNotBiggerThanY(0, 100),
    #     'p_reproductionThreshold': getRandIntBiggerThanY(0, 100, reproduction_value[1]),
    #     'd_strength': getRandIntXLessThanY(0, 100),
    #     'd_rate': getRandIntXLessThanY(0, 100),
    #     'd_death': randint(0, 100),
    #     'maxGen': maxGen
    # }

    print('-----------')
    print('[' + str(i) + ']')
    print("settings:")
    print(settings)
    print('-----------')

    data = _setup.run(settings)

    # remove unwanted data
    for gen in data:
        for day in gen['data']:
            for colony in day['colonies']:
                for person in day['colonies'][colony]['people']:
                    if hasattr(person, 'color'):
                        del person.color
                        del person._map
                        del person._setPixelColorBack
                        del person._settings
                        del person._colonyName
                        del person._colonyID
                        if person._disease:
                            del person._disease._settings
                            del person._disease.allKinds

    new_data = {'settings': settings, 'data': data}

    serialized_data = json.dumps(new_data, default=lambda o: o.__dict__)
    # db.save(json.loads(serialized_data))
    with open("test_data2.json", "w") as f:
        json.dump(json.loads(serialized_data), f)
    print('[' + str(i) + '] saved')
