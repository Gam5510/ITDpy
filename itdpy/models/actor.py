from typing import Optional
from pydantic import Field
from .base import ITDBaseModel

class Actor(ITDBaseModel):
    id: str
    username: Optional[str] = None
    display_name: Optional[str] = Field(None, alias="displayName")
    avatar: Optional[str] = None

    def __repr__(self):
        return f"<Actor @{self.username}>"
