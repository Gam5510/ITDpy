from __future__ import annotations

from typing import Optional

from pydantic import Field

from .base import ITDBaseModel


class VerificationRequest(ITDBaseModel):
    id: str
    user_id: str = Field(alias="userId")
    video_url: str = Field(alias="videoUrl")
    status: str  # pending / approved / rejected
    rejection_reason: Optional[str] = Field(None, alias="rejectionReason")
    reviewed_by: Optional[str] = Field(None, alias="reviewedBy")
    reviewed_at: Optional[str] = Field(None, alias="reviewedAt")
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")


class VerificationStatus(ITDBaseModel):
    is_verified: bool = Field(False, alias="isVerified")
    request: Optional[VerificationRequest] = None
