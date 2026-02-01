from typing import List, Optional
from pydantic import Field
from .base import ITDBaseModel
from .user_lite import UserLite
from .attachment import Attachment

class Comment(ITDBaseModel):
    id: str
    content: Optional[str] = None
    
    likes_count: int = Field(0, alias="likesCount", validation_alias="likkesCount")
    replies_count: int = Field(0, alias="repliesCount")
    is_liked: bool = Field(False, alias="isLiked")
    
    created_at: str = Field(..., alias="createdAt")
    
    author: Optional[UserLite] = None
    attachments: List[Attachment] = []
    replies: List["Comment"] = []
