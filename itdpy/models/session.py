from __future__ import annotations

from typing import Optional, List

from pydantic import Field

from .base import BaseList, ITDBaseModel, parse_list


class Session(ITDBaseModel):

    id: str
    is_current: bool = Field(False, alias="isCurrent")

    created_at: str = Field(alias="createdAt")
    last_used_at: str = Field(alias="lastUsedAt")
    expires_at: str = Field(alias="expiresAt")

    ip_address: Optional[str] = Field(None, alias="ipAddress")
    ip_country: Optional[str] = Field(None, alias="ipCountry")
    ip_city: Optional[str] = Field(None, alias="ipCity")

    device_type: Optional[str] = Field(None, alias="deviceType")
    os_name: Optional[str] = Field(None, alias="osName")
    os_version: Optional[str] = Field(None, alias="osVersion")
    device_model: Optional[str] = Field(None, alias="deviceModel")

    client_name: Optional[str] = Field(None, alias="clientName")
    client_version: Optional[str] = Field(None, alias="clientVersion")

    @property
    def location(self) -> Optional[str]:
        if self.ip_country and self.ip_city:
            return f"{self.ip_city}, {self.ip_country}"
        return self.ip_country or self.ip_city

    def __str__(self) -> str:
        parts = []
        if self.os_name:
            parts.append(self.os_name)
            if self.os_version:
                parts.append(str(self.os_version))
        if self.device_type:
            parts.append(f"({self.device_type})")
        if self.client_name:
            parts.append(f"{self.client_name}/{self.client_version or '?'}")
        return " ".join(parts) if parts else self.id


class SessionsList(BaseList[Session]):

    def __init__(self, items: Optional[List[Session]] = None, *, revoked_count: Optional[int] = None):
        super().__init__(items)
        self.revoked_count = revoked_count

    @classmethod
    def from_data(cls, data: dict | list) -> "SessionsList":
        payload = data
        revoked_count = None

        if isinstance(payload, dict):
            revoked_count = payload.get("revokedCount")
            payload = payload.get("sessions", payload.get("data", payload))

        if isinstance(payload, list):
            items = payload
        else:
            items = []

        return cls(parse_list(Session, items).to_list(), revoked_count=revoked_count)
