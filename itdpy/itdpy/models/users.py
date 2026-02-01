from typing import List, Optional, Any
from pydantic import Field, model_validator
from .base import ITDBaseModel
from .user_lite import UserLite

class Users(ITDBaseModel):
    users: List[UserLite] = Field(default_factory=list)
    page: Optional[int] = None
    limit: Optional[int] = None
    total: Optional[int] = None
    has_more: Optional[bool] = Field(None, alias="hasMore")
    
    @model_validator(mode='before')
    @classmethod
    def parse_structure(cls, data: Any) -> Any:
        if isinstance(data, dict):
            root_data = data.get("data", {})
            users_list = root_data.get("users", [])
            pagination = root_data.get("pagination", {})
            
            return {
                "users": users_list,
                "page": pagination.get("page"),
                "limit": pagination.get("limit"),
                "total": pagination.get("total"),
                "hasMore": pagination.get("hasMore")
            }
        return {"users": []}

    def __getitem__(self, index):
        return self.users[index]

    def __len__(self):
        return len(self.users)

    def __iter__(self):
        return iter(self.users)

    def __repr__(self):
        return f"<Users count={len(self)}>"
