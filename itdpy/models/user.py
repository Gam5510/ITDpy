from typing import Optional
from pydantic import Field
from .user_lite import UserLite

class User(UserLite):
    banner: Optional[str] = None
    bio: Optional[str] = None
    pinned_post_id: Optional[str] = Field(None, alias="pinnedPostId")
    wall_closed: bool = Field(False, alias="wallClosed")
    
    followers_count: int = Field(0, alias="followersCount")
    following_count: int = Field(0, alias="followingCount")
    posts_count: int = Field(0, alias="postsCount")
    
    is_followed_by: bool = Field(False, alias="isFollowedBy")
    created_at: Optional[str] = Field(None, alias="createdAt")
