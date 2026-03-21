from pydantic import Field
from typing import Literal
from .base import ITDBaseModel


class PrivacySettings(ITDBaseModel):
    is_private: bool = Field(alias="isPrivate")
    wall_access: Literal["nobody", "everyone", "followers", "mutual"] = Field(alias="wallAccess")
    likes_visibility: Literal["nobody", "everyone", "followers", "mutual"]  = Field(alias="likesVisibility")
    show_last_seen: bool = Field(alias="showLastSeen")

    
class NotificationSettings(ITDBaseModel):
    enabled: bool
    comments: bool
    follows: bool
    likes: bool
    mentions: bool
    sound: bool
    wall_posts: bool = Field(alias="wallPosts")
