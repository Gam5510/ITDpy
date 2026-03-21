from __future__ import annotations
from typing import List
from pydantic import Field, model_validator
from .base import BaseList, ITDBaseModel, parse_list
from .who_to_follow import SuggestedUser
from .hashtags import Hashtag


class Search(ITDBaseModel):
    users: List[SuggestedUser] = Field(default_factory=list)
    hashtags: List[Hashtag] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def unwrap_data(cls, payload):
        if isinstance(payload, dict) and "data" in payload:
            return payload["data"]
        return payload

class SearchUsersResponse(BaseList[SuggestedUser]):
    def __init__(self, items: List[SuggestedUser] | None = None):
        super().__init__(items)

    @classmethod
    def from_data(cls, data: list[SuggestedUser] | list[dict]) -> "SearchUsersResponse":
        return cls(parse_list(SuggestedUser, data).to_list())


class SearchHashtagsResponse(BaseList[Hashtag]):
    def __init__(self, items: List[Hashtag] | None = None):
        super().__init__(items)

    @classmethod
    def from_data(cls, data: list[Hashtag] | list[dict]) -> "SearchHashtagsResponse":
        return cls(parse_list(Hashtag, data).to_list())
