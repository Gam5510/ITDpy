class BaseModel:
    def __init__(self, data: dict):
        self._data = data

    def to_dict(self):
        return self._data
