from __future__ import annotations

from typing import Optional, List

from pydantic import Field

from .base import BaseList, ITDBaseModel, parse_list


class Subscription(ITDBaseModel):

    id: Optional[str] = None
    status: Optional[str] = None
    plan: Optional[str] = None
    started_at: Optional[str] = Field(None, alias="startedAt")
    expires_at: Optional[str] = Field(None, alias="expiresAt")
    auto_renewal: Optional[bool] = Field(None, alias="autoRenewal")
    is_active: Optional[bool] = Field(None, alias="isActive")


class PaymentMethod(ITDBaseModel):

    id: str
    type: Optional[str] = None
    last_four: Optional[str] = Field(None, alias="lastFour")
    brand: Optional[str] = None
    is_default: Optional[bool] = Field(None, alias="isDefault")
    expires_at: Optional[str] = Field(None, alias="expiresAt")


class PaymentMethodsList(BaseList[PaymentMethod]):
    @classmethod
    def from_data(cls, data: dict | list) -> "PaymentMethodsList":
        if isinstance(data, dict):
            data = data.get("methods", data.get("data", []))
        if isinstance(data, list):
            return cls(parse_list(PaymentMethod, data).to_list())
        return cls([])
