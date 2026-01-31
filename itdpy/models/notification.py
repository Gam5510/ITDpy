from .actor import Actor

class Notification:
    def __init__(self, data: dict):
        self.id = data.get("id")
        self.type = data.get("type")              # comment | like | follow | reply
        self.target_type = data.get("targetType") # post | None
        self.target_id = data.get("targetId")
        self.preview = data.get("preview")

        self.read = data.get("read")
        self.read_at = data.get("readAt")
        self.created_at = data.get("createdAt")

        actor_data = data.get("actor")
        self.actor = Actor(actor_data) if actor_data else None

    def __repr__(self):
        return f"<Notification {self.type} from @{self.actor.username if self.actor else '?'}>"
