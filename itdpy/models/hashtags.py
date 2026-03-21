from pydantic import Field, model_validator
from typing import List, Any
from .base import BaseList, ITDBaseModel, parse_list, parse_model
from .post import Post
from .pagination import Pagination


class Hashtag(ITDBaseModel):
    id: str
    name: str
    posts_count: int = Field(alias="postsCount")

class HashtagPosts(BaseList[Post]):
    def __init__(
        self,
        items: List[Post] | None = None,
        *,
        hashtag: Hashtag,
        pagination: Pagination | None = None,
    ):
        super().__init__(items)
        self.hashtag = hashtag
        self.pagination = pagination

    @model_validator(mode="before")
    @classmethod
    def flatten_data(cls, payload: Any):
        if isinstance(payload, dict) and "data" in payload:
            return payload["data"]
        return payload

    @classmethod
    def from_data(cls, payload: Any) -> "HashtagPosts":
        flattened = cls.flatten_data(payload)
        return cls(
            parse_list(Post, flattened.get("posts", [])).to_list(),
            hashtag=parse_model(Hashtag, flattened["hashtag"]),
            pagination=parse_model(Pagination, flattened["pagination"]) if flattened.get("pagination") else None,
        )

    @property
    def posts(self) -> List[Post]:
        return self.items
    
class TrendingHashtagsResponse(BaseList[Hashtag]):
    def __init__(self, items: list[Hashtag] | None = None):
        super().__init__(items)

    @classmethod
    def from_data(cls, data: dict) -> "TrendingHashtagsResponse":
        return cls(parse_list(Hashtag, data.get("hashtags", [])).to_list())

    @property
    def hashtags(self) -> list[Hashtag]:
        return self.items
