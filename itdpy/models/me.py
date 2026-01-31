from .user import User
import json

class Me(User):
    def __init__(self, data: dict):
        super().__init__(data)
        self.data = data

        self.isPrivate = data.get("isPrivate")

    def __str__(self):
        return json.dumps(self.data, ensure_ascii=False)