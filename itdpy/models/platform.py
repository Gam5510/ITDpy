from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from .base import BaseList, ITDBaseModel, parse_list


class App(ITDBaseModel):

    name: str
    min_version: Optional[str] = Field(None, alias="minVersion")
    version: Optional[str] = Field(None, alias="latestVersion")
    update_url: Optional[str] = Field(None, alias="updateUrl")

    @property
    def version_tuple(self) -> Optional[tuple]:
        if self.version:
            try:
                return tuple(map(int, self.version.split(".")))
            except ValueError:
                return None
        return None


class Version(ITDBaseModel):

    version: str
    date: Optional[str] = None
    changes: List[str] = Field(default_factory=list)

    @property
    def version_tuple(self) -> tuple:
        try:
            return tuple(map(int, self.version.split(".")))
        except ValueError:
            return (0,)


class Changelog(BaseList[Version]):

    @classmethod
    def from_data(cls, data: dict | list) -> "Changelog":
        if isinstance(data, dict):
            data = data.get("data", data.get("changelog", []))
        if isinstance(data, list):
            return cls(parse_list(Version, data).to_list())
        return cls([])
