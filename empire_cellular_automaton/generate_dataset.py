import json
import setup

_setup = setup.setup()


settings = {
    'p_strength': [0, 100],
    'p_reproductionValue': [0, 70],
    'p_disease': [0, 10, 0],
    'p_child_disease': [0, 10, 0],
    'p_reproductionThreshold': 115,
    'd_strength': [0, 100],
    'd_rate': [0, 10],
    'd_death': 100
}


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

serialized_data = json.dumps(data, default=lambda o: o.__dict__)
with open('test.json', 'w') as f:
    json.dump(serialized_data, f)
