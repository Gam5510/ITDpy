from .auth import AuthManager

def validate_and_refresh(auth: AuthManager) -> bool:
    if not auth.client.access_token:
        return False

    r = auth.client.get("/api/users/me")

    if r.status_code == 200:
        return True

    if r.status_code == 401:
        return bool(auth.refresh_access_token())

    return False
