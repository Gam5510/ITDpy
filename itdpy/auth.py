from .client import ITDClient


class AuthManager:
    def __init__(self, client: ITDClient):
        self.client = client
        self.client._bind_auth_manager(self)

    def _has_refresh_token(self) -> bool:
        return any(
            c.name == "refresh_token"
            for c in self.client.session.cookies
        )

    def refresh_access_token(self) -> str | None:

        if not self._has_refresh_token():
            raise RuntimeError("refresh_token not found in cookies")

        r = self.client.post("/api/v1/auth/refresh")
        if r.status_code != 200:
            return None

        token = r.json().get("accessToken")
        if not token:
            return None

        self.client._set_access_token(token)

        self._bootstrap_identity()

        return token

    def _bootstrap_identity(self):
        r = self.client.get("/api/users/me")
        if r.status_code != 200:
            return

        user_id = r.json().get("id")
        if user_id:
            self.client._set_user_id(user_id)
