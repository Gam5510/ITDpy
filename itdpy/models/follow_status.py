from pydantic import Field

from .base import ITDBaseModel


class FollowStatusItem(ITDBaseModel):
    id: str
    is_following: bool = Field(False, alias="isFollowing")


class PostViewResponse(ITDBaseModel):
    viewed: bool = True
