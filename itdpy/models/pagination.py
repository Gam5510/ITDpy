from typing import Optional, Union
from pydantic import AliasChoices, Field

from .base import ITDBaseModel


class Pagination(ITDBaseModel):
    page: Optional[int] = 1
    limit: Optional[int] = 20
    total: Optional[int] = 0
    cursor: Optional[str | int | None] = Field(
        default=None,
        validation_alias=AliasChoices("cursor", "nextCursor"),
    )
    has_more: Optional[bool] = Field(False, alias="hasMore")

    
