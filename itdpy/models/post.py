from .user_lite import UserLite
from .attachment import Attachment
from .comment import Comment
import json

class Post:
    def __init__(self, data: dict):

        if "data" in data:
            data = data["data"]

        self._data = data

        self.id = data.get("id")
        self.content = data.get("content")
        self.likesCount = data.get("likesCount")
        self.commentsCount = data.get("commentsCount")
        self.repostsCount = data.get("repostsCount")
        self.viewsCount = data.get("viewsCount")
        self.isLiked = data.get("isLiked")
        self.isReposted = data.get("isReposted")
        self.isViewed = data.get("isViewed")
        self.isOwner = data.get("isOwner")
        self.createdAt = data.get("createdAt")

        self.author = UserLite(data.get("author"))

        self.attachments = [
            Attachment(a) for a in data.get("attachments", [])
        ]

        self.comments = [
            Comment(c) for c in data.get("comments", [])
        ]

        # wall
        self.wallRecipientId = data.get("wallRecipientId")
        self.wallRecipient = (
            UserLite(data["wallRecipient"])
            if data.get("wallRecipient") else None
        )

    def __repr__(self):
        return f"<Post {self.id}>"
    
    def __str__(self):
        return json.dumps(self._data, ensure_ascii=False)
