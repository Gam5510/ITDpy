from typing import Optional

from pydantic import AliasChoices, Field

from .base import BaseList, ITDBaseModel, parse_list
from .pin import Pin

class UserLite(ITDBaseModel):
    id: Optional[str] = None
    username: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("username", "userrname"),
    )
    display_name: Optional[str] = Field(None, alias="displayName")

    avatar: Optional[str] = Field(None, alias="avatar")
    is_verified: bool = Field(
        False,
        alias="isVerified",
        validation_alias=AliasChoices("isVerified", "verified", "verifieed"),
        serialization_alias="isVerified",
    )
    is_following: bool = Field(
        False,
        alias="isFollowing",
        validation_alias=AliasChoices("isFollowing", "following"),
        serialization_alias="isFollowing",
    )
    is_followed_by: bool = Field(
        False,
        alias="isFollowedBy",
        validation_alias=AliasChoices("isFollowedBy", "followedBy"),
        serialization_alias="isFollowedBy",
    )
    has_nuksta: Optional[bool] = Field(None, alias="hasNuksta")
    pin: Optional[Pin] = None


class User(UserLite):
    bio: Optional[str] = None
    banner_url: Optional[str] = Field(None, alias="bannerUrl")

    followers_count: int = Field(0, alias="followersCount")
    following_count: int = Field(0, alias="followingCount")
    posts_count: int = Field(0, alias="postsCount")

    created_at: Optional[str] = Field(None, alias="createdAt")


class UsersList(BaseList[User]):
    def __init__(
        self,
        items: list[User] | None = None,
        *,
        total: Optional[int] = None,
        page: Optional[int] = None,
        has_more: bool = False,
    ):
        super().__init__(items)
        self.total = total
        self.page = page
        self.has_more = has_more

    @classmethod
    def from_data(cls, data: dict | list) -> "UsersList":
        payload = data
        total: Optional[int] = None
        page: Optional[int] = None
        has_more = False

        if isinstance(payload, dict) and "data" in payload:
            payload = payload["data"]

        if isinstance(payload, list):
            items = payload
        elif isinstance(payload, dict):
            if isinstance(payload.get("items"), list):
                items = payload.get("items", [])
            elif isinstance(payload.get("users"), list):
                items = payload.get("users", [])
            elif "id" in payload:
                items = [payload]
            else:
                items = []

            total = payload.get("total")
            page = payload.get("page")
            has_more = payload.get("hasMore", False)

            if isinstance(payload.get("pagination"), dict):
                total = payload["pagination"].get("total", total)
                page = payload["pagination"].get("page", page)
                has_more = payload["pagination"].get("hasMore", has_more)
        else:
            items = []

        return cls(
            parse_list(User, items).to_list(),
            total=total,
            page=page,
            has_more=has_more,
        )


class Actor(ITDBaseModel):
    id: str
    username: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("username", "userrname"),
    )
    display_name: Optional[str] = Field(None, alias="displayName")
    avatar: Optional[str] = None
    is_verified: bool = Field(
        False,
        alias="isVerified",
        validation_alias=AliasChoices("isVerified", "verified", "verifieed"),
        serialization_alias="isVerified",
    )
    pin: Optional[Pin] = None


class Me(User):
    is_private: Optional[bool] = Field(None, alias="isPrivate")
