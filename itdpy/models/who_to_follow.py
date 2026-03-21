from pydantic import Field
from typing import List
from .base import BaseList, ITDBaseModel, parse_list


class SuggestedUser(ITDBaseModel):
    id: str
    username: str
    display_name: str = Field(alias="displayName")
    avatar: str
    verified: bool
    followers_count: int = Field(alias="followersCount")

class WhoToFollow(BaseList[SuggestedUser]):
    def __init__(self, items: List[SuggestedUser] | None = None):
        super().__init__(items)

    @classmethod
    def from_data(cls, data: dict) -> "WhoToFollow":
        return cls(parse_list(SuggestedUser, data.get("users", [])).to_list())

    @property
    def users(self) -> List[SuggestedUser]:
        return self.items

