from typing import List, Optional, Union, Any
from pydantic import Field, model_validator
from .base import ITDBaseModel
from .post import Post

class Posts(ITDBaseModel):
    posts: List[Post] = Field(default_factory=list)
    limit: Optional[int] = None
    next_cursor: Optional[str] = Field(None, alias="nextCursor")
    has_more: Optional[bool] = Field(None, alias="hasMore")
    
    @model_validator(mode='before')
    @classmethod
    def parse_structure(cls, data: Any) -> Any:
        if isinstance(data, dict) and "data" in data:
            data = data["data"]
            
        if isinstance(data, list):
            return {"posts": data}
            
        if isinstance(data, dict):

            posts_list = data.get("posts", [])
            pagination = data.get("pagination", {})
            
            return {
                "posts": posts_list,
                "limit": pagination.get("limit"),
                "nextCursor": pagination.get("nextCursor"),
                "hasMore": pagination.get("hasMore")
            }
            
        return {"posts": []}

    def __iter__(self):
        return iter(self.posts)

    def __getitem__(self, item):
        return self.posts[item]

    def __len__(self):
        return len(self.posts)

    def __repr__(self):
        return f"<Posts count={len(self)}>"
