import requests


class ITDClient:

    _DEFAULT_TIMEOUT = 15
    _UPLOAD_TIMEOUT = 3600
    _SDK_NAME = "itd-sdk-python"
    _SDK_VERSION = "0.1"
    _PLATFORM = "python"
    

    def __init__(self, refresh_token: str):
        self.base_url = "https://xn--d1ah4a.com"
        self.session = requests.Session()

        self._access_token = None
        self._user_id = None
        self._auth_manager = None

        self.session.headers.update({
            "Origin": self.base_url,
            "Referer": self.base_url + "/"
        })

        self.session.cookies.set(
            name="refresh_token",
            value=refresh_token,
            domain="xn--d1ah4a.com",
            path="/api"
        )

        self._apply_user_agent(initial=True)

    def _bind_auth_manager(self, auth_manager):
        self._auth_manager = auth_manager

    def _set_access_token(self, token: str):
        self._access_token = token
        self.session.headers["Authorization"] = f"Bearer {token}"

    def _set_user_id(self, user_id: str):
        self._user_id = user_id
        self._apply_user_agent()

    def _build_user_agent(self, initial: bool = False) -> str:
        if initial or not self._user_id:
            return (
                f"{self._SDK_NAME}/{self._SDK_VERSION} "
                f"(initial; platform={self._PLATFORM})"
            )

        return (
            f"{self._SDK_NAME}/{self._SDK_VERSION} "
            f"(userid={self._user_id}; platform={self._PLATFORM})"
        )

    def _apply_user_agent(self, initial: bool = False):
        # всегда перезаписываем — анти-подмена
        self.session.headers["User-Agent"] = self._build_user_agent(initial)

    def _request(self, method: str, path: str, retry: bool = True, **kwargs):
        self._apply_user_agent()

        if not path.startswith("/"):
            path = "/" + path

        url = self.base_url + path

        timeout = kwargs.pop("timeout", None)
        if timeout is None:
            if path.startswith("/api/files"):
                timeout = self._UPLOAD_TIMEOUT
            else:
                timeout = self._DEFAULT_TIMEOUT

        response = self.session.request(
            method,
            url,
            timeout=timeout,
            **kwargs
        )

        if response.status_code == 401 and retry and self._auth_manager:
            refreshed = self._auth_manager.refresh_access_token()
            if refreshed:
                return self._request(method, path, retry=False, **kwargs)

        return response


    def get(self, path: str, **kwargs):
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs):
        return self._request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs):
        return self._request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self._request("DELETE", path, **kwargs)
