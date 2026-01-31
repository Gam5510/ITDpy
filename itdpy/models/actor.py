class Actor:
    def __init__(self, data: dict):
        self.id = data.get("id")
        self.username = data.get("username")
        self.displayName = data.get("displayName")
        self.avatar = data.get("avatar")

    def __repr__(self):
        return f"<Actor @{self.username}>"
