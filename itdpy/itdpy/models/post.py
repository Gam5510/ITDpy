from typing import List, Optional, Any
from pydantic import Field, model_validator
from .base import ITDBaseModel
from .user_lite import UserLite
from .attachment import Attachment
from .comment import Comment

class Post(ITDBaseModel):
    @model_validator(mode='before')
    @classmethod
    def unwrap_data(cls, data: Any) -> Any:
        if isinstance(data, dict) and "data" in data and len(data) == 1:
             return data["data"]
        if isinstance(data, dict) and "data" in data and isinstance(data["data"], dict) and "id" in data["data"]:
             return data["data"]
        return data

    id: str
    content: Optional[str] = None
    
    likes_count: int = Field(0, alias="likesCount", validation_alias="likkesCount")
    comments_count: int = Field(0, alias="commentsCount")
    reposts_count: int = Field(0, alias="repostsCount")
    views_count: int = Field(0, alias="viewsCount")
    
    is_liked: bool = Field(False, alias="isLiked")
    is_reposted: bool = Field(False, alias="isReposted")
    is_viewed: bool = Field(False, alias="isViewed")
    is_owner: bool = Field(False, alias="isOwner")
    
    created_at: str = Field(..., alias="createdAt")
    
    author: Optional[UserLite] = None
    
    attachments: List[Attachment] = []
    comments: List[Comment] = []
    
    # wall
    wall_recipient_id: Optional[str] = Field(None, alias="wallRecipientId")
    wall_recipient: Optional[UserLite] = Field(None, alias="wallRecipient")

    def __repr__(self):
        return f"<Post {self.id}>"
