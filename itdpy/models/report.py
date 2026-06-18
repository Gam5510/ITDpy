from __future__ import annotations

from typing import Optional

from pydantic import Field

from .base import ITDBaseModel


class Report(ITDBaseModel):

    id: Optional[str] = None
    target_id: Optional[str] = Field(None, alias="targetId")
    target_type: Optional[str] = Field(None, alias="targetType")
    reason: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = Field(None, alias="createdAt")
