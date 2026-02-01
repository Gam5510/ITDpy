from typing import Optional
from pydantic import Field
from .user import User

class Me(User):
    is_private: Optional[bool] = Field(None, alias="isPrivate")
