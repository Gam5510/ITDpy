from __future__ import annotations
from ..models import Pins, PinStatusResponse
from ..api.base import BaseAPI

class PinsAPI(BaseAPI):

    def get(self):
        response = self._get("users/me/pins")
        return Pins.from_data(response.json())

    def remove(self):
        response = self._delete("users/me/pin")
        return PinStatusResponse.model_validate(response.json())
    
    def set(self, slug):
        payload = {'slug': slug}
        response = self._put("users/me/pin", json=payload)
        return PinStatusResponse.model_validate(response.json())

