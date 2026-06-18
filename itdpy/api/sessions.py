from ..api.base import BaseAPI
from ..models import SessionsList


class SessionsAPI(BaseAPI):

    def list(self) -> SessionsList:
        response = self._get("v1/auth/sessions")
        return SessionsList.from_data(response.json())

    def revoke(self, session_id: str) -> None:
        self._delete(f"v1/auth/sessions/{session_id}")

    def revoke_all(self) -> int:
        response = self._delete("v1/auth/sessions")
        data = response.json()
        if isinstance(data, dict):
            return data.get("revokedCount", 0)
        return 0
