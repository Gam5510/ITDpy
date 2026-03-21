from typing import Optional

from pydantic import Field

from .base import ITDBaseModel


class File(ITDBaseModel):
    id: str
    url: str
    type: Optional[str] = None

    filename: Optional[str] = None
    mime_type: Optional[str] = Field(None, alias="mimeType")

    size: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None

    created_at: Optional[str] = Field(None, alias="createdAt")
