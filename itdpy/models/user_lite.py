from typing import Optional
from pydantic import Field
from .base import ITDBaseModel

class UserLite(ITDBaseModel):
    id: str
    username: Optional[str] = None
    display_name: Optional[str] = Field(None, alias="displayName")
    avatar: Optional[str] = None
    verified: bool = False
    is_following: bool = Field(False, alias="isFollowing")
