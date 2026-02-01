from typing import Optional
from pydantic import Field
from .base import ITDBaseModel
from .actor import Actor

class Notification(ITDBaseModel):
    id: str
    type: str 
    target_type: Optional[str] = Field(None, alias="targetType") 
    target_id: Optional[str] = Field(None, alias="targetId")
    preview: Optional[str] = None
    
    read: bool = False
    read_at: Optional[str] = Field(None, alias="readAt")
    created_at: str = Field(..., alias="createdAt")
    
    actor: Optional[Actor] = None

    def __repr__(self):
        return f"<Notification {self.type} from @{self.actor.username if self.actor and self.actor.username else '?'}>"
