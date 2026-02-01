from typing import List, Optional, Any
from pydantic import Field, model_validator
from .base import ITDBaseModel
from .notification import Notification

class Notifications(ITDBaseModel):
    notifications: List[Notification] = Field(default_factory=list)
    has_more: bool = Field(False, alias="hasMore")
    
    @model_validator(mode='before')
    @classmethod
    def parse_structure(cls, data: Any) -> Any:
        if isinstance(data, dict):
            return {
                "notifications": data.get("notifications", []),
                "hasMore": data.get("hasMore", False)
            }
        return {"notifications": [], "hasMore": False}

    def __iter__(self):
        return iter(self.notifications)

    def __getitem__(self, item):
        return self.notifications[item]

    def __len__(self):
        return len(self.notifications)

    def __repr__(self):
        return f"<Notifications count={len(self)}>"
