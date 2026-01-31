import json
from .user_lite import UserLite


class User(UserLite):
    def __init__(self, data: dict):
        super().__init__(data)

        self.banner = data.get("banner")
        self.bio = data.get("bio")
        self.pinnedPostId = data.get("pinnedPostId")
        self.wallClosed = data.get("wallClosed")
        self.followersCount = data.get("followersCount")
        self.followingCount = data.get("followingCount")
        self.postsCount = data.get("postsCount")
        self.isFollowing = data.get("isFollowing")
        self.isFollowedBy = data.get("isFollowedBy")
        self.createdAt = data.get("createdAt")

        self._data = data

    def __str__(self):
        return json.dumps(self._data, ensure_ascii=False)
