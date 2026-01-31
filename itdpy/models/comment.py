from .user_lite import UserLite
from .attachment import Attachment
import json

class Comment:
    def __init__(self, data: dict):
        self.id = data.get("id")
        self.content = data.get("content")
        self.likesCount = data.get("likesCount")
        self.repliesCount = data.get("repliesCount")
        self.isLiked = data.get("isLiked")
        self.createdAt = data.get("createdAt")

        self.author = UserLite(data.get("author"))
        self.attachments = [
            Attachment(a) for a in data.get("attachments", [])
        ]

        self.replies = [
            Comment(r) for r in data.get("replies", [])
        ]

        self.data = data
    
    def __str__(self):
        return json.dumps(self.data, ensure_ascii=False)
