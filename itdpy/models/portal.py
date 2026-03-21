from pydantic import Field

from .base import ITDBaseModel


class Portal(ITDBaseModel):
    active: bool
    title: str
    url: str
