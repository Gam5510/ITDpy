from typing import TYPE_CHECKING, List, Optional

from pydantic import AliasChoices, Field

from .base import BaseList, ITDBaseModel, parse_list
from .post import Attachment

if TYPE_CHECKING:
    from .user import UserLite


class Comment(ITDBaseModel):
    id: str
    content: str

    likes_count: int = Field(0, alias="likesCount")
    replies_count: int = Field(0, alias="repliesCount")

    is_liked: bool = Field(False, alias="isLiked")
    is_owner: bool = Field(False, alias="isOwner")

    created_at: str = Field(alias="createdAt")

    author: Optional["UserLite"] = None
    attachments: List[Attachment] = Field(default_factory=list)
    post_id: Optional[str] = Field(None, alias="postId")


class CommentsList(BaseList[Comment]):
    def __init__(
        self,
        items: List[Comment] | None = None,
        *,
        total: Optional[int] = None,
        next_cursor: Optional[str] = None,
        has_more: bool = False,
    ):
        super().__init__(items)
        self.total = total
        self.next_cursor = next_cursor
        self.has_more = has_more

    @classmethod
    def from_data(cls, data: dict | list) -> "CommentsList":
        payload = data
        total: Optional[int] = None
        next_cursor: Optional[str] = None
        has_more = False

        if isinstance(payload, dict) and "data" in payload:
            payload = payload["data"]

        if isinstance(payload, list):
            items = payload
        elif isinstance(payload, dict):
            if isinstance(payload.get("items"), list):
                items = payload.get("items", [])
            elif isinstance(payload.get("comments"), list):
                items = payload.get("comments", [])
            elif "id" in payload and "createdAt" in payload:
                items = [payload]
            else:
                items = []

            total = payload.get("total")
            next_cursor = payload.get("nextCursor")
            has_more = payload.get("hasMore", False)

            if isinstance(payload.get("pagination"), dict):
                total = payload["pagination"].get("total", total)
                next_cursor = payload["pagination"].get("nextCursor")
                has_more = payload["pagination"].get("hasMore", False)
        else:
            items = []

        return cls(
            parse_list(Comment, items).to_list(),
            total=total,
            next_cursor=next_cursor,
            has_more=has_more,
        )


class CommentUpdate(ITDBaseModel):
    id: str
    content: Optional[str] = None
    updated_at: str = Field(
        ...,
        validation_alias=AliasChoices("updatedAt", "editedAt"),
        serialization_alias="editedAt",
    )
