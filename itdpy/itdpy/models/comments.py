from typing import List, Optional
from pydantic import BaseModel, Field
from .base import ITDBaseModel
from .comment import Comment

class CommentsData(ITDBaseModel):
    comments: List[Comment]
    total: int
    has_more: bool = Field(..., alias="hasMore")
    next_cursor: Optional[str] = Field(None, alias="nextCursor")

class Comments(ITDBaseModel):
    data: CommentsData

    def __iter__(self):
        return iter(self.data.comments)

    def __getitem__(self, item):
        return self.data.comments[item]

    def __len__(self):
        return len(self.data.comments)
