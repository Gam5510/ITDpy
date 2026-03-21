from pydantic import Field

from .base import BaseList, ITDBaseModel, parse_list


class Clan(ITDBaseModel):
    avatar: str
    member_count: int = Field(alias="memberCount")


class TopClansResponse(BaseList[Clan]):
    def __init__(self, items: list[Clan] | None = None):
        super().__init__(items)

    @classmethod
    def from_data(cls, data: dict) -> "TopClansResponse":
        return cls(parse_list(Clan, data.get("clans", [])).to_list())

    @property
    def clans(self) -> list[Clan]:
        return self.items
