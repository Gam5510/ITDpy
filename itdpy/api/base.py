"""Base API class"""

from typing import Optional, Dict, Any
import requests

from ..request import RequestHandler


class BaseAPI:

    def __init__(self, request_handler: RequestHandler, access_token: str):
        self._request = request_handler
        self._token = access_token
    
    def _get(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request.request("GET", endpoint, access_token=self._token, **kwargs)
    
    def _post(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request.request("POST", endpoint, access_token=self._token, **kwargs)
    
    def _put(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request.request("PUT", endpoint, access_token=self._token, **kwargs)

    def _patch(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request.request("PATCH", endpoint, access_token=self._token, **kwargs)
    
    def _delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request.request("DELETE", endpoint, access_token=self._token, **kwargs)
