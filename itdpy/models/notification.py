from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import Field

from .base import BaseList, ITDBaseModel, parse_list
from ..enums import NotificationType, NotificationTargetType

class NotificationActor(ITDBaseModel):
    id: str
    display_name: str = Field(alias="displayName")
    username: str
    avatar: Optional[str] = None
    is_following: bool = Field(False, alias="isFollowing")
    is_followed_by: bool = Field(False, alias="isFollowedBy")


class ConnectedEventData(ITDBaseModel):
    user_id: str = Field(alias="userId")
    timestamp: int


class Notification(ITDBaseModel):
    id: str
    type: NotificationType
    target_type: Optional[NotificationTargetType] = Field(None, alias="targetType")
    target_id: Optional[str] = Field(None, alias="targetId")
    preview: Optional[str] = None
    read_at: Optional[str] = Field(None, alias="readAt")
    created_at: str = Field(alias="createdAt")
    user_id: Optional[str] = Field(None, alias="userId")
    actor: NotificationActor
    read: bool = False
    sound: bool = False


class NotificationsList(BaseList[Notification]):
    def __init__(self, items: List[Notification] | None = None, *, total: Optional[int] = None):
        super().__init__(items)
        self.total = total

    @classmethod
    def from_data(cls, data: dict | list) -> "NotificationsList":
        payload = data
        total: Optional[int] = None

        if isinstance(payload, dict) and "data" in payload:
            payload = payload["data"]

        if isinstance(payload, list):
            items = payload
        elif isinstance(payload, dict):
            if isinstance(payload.get("items"), list):
                items = payload.get("items", [])
            elif isinstance(payload.get("notifications"), list):
                items = payload.get("notifications", [])
            elif "id" in payload and "createdAt" in payload:
                items = [payload]
            else:
                items = []
            total = payload.get("total")
        else:
            items = []

        return cls(
            parse_list(Notification, items).to_list(),
            total=total,
        )
