import json

class UserLite:
    def __init__(self, data: dict):
        self._data = data or {}

        self.id = data.get("id")
        self.username = data.get("username")
        self.displayName = data.get("displayName")
        self.avatar = data.get("avatar")
        self.verified = data.get("verified")
        self.isFollowing = data.get("isFollowing")

    def __repr__(self):
        return f"<UserLite @{self.username}>"
    
    def __str__(self):
        return json.dumps(self._data, ensure_ascii=False)