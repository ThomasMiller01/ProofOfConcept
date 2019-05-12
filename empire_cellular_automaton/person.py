class Person:
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    _id = None
    _colonyID = None
    _age = None
    _strength = None
    _reproductionValue = None
