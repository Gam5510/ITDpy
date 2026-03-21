from typing import Any, Optional

from pydantic import Field

from .base import BaseList, ITDBaseModel, StatusResponse, parse_list

class Pin(ITDBaseModel):
    slug: str
    name: str
    description: Optional[str] = None
    granted_at: Optional[str] = Field(None, alias="grantedAt")


class Pins(BaseList[Pin]):
    def __init__(self, items: list[Pin] | None = None, *, active_pin: Optional[str] = None):
        super().__init__(items)
        self.active_pin = active_pin

    @classmethod
    def from_data(cls, data: Any) -> "Pins":
        if isinstance(data, dict) and "data" in data:
            data = data["data"]

        if isinstance(data, dict):
            return cls(
                parse_list(Pin, data.get("pins", [])).to_list(),
                active_pin=data.get("activePin"),
            )

        return cls([], active_pin=None)

    @property
    def pins(self) -> list[Pin]:
        return self.items


class PinStatusResponse(StatusResponse):
    active_pin: Optional[str] = Field(None, alias="activePin")
