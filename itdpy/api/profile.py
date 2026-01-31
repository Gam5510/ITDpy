from ..models.me import Me


def update_profile(client, *, display_name: str | None = None, username: str | None = None, bio: str | None = None, banner_id: str | None = None) -> Me:
    payload = {}

    if display_name is not None:
        payload["displayName"] = display_name

    if username is not None:
        payload["username"] = username

    if bio is not None:
        payload["bio"] = bio

    if banner_id is not None:
        payload["bannerId"] = banner_id

    if not payload:
        raise ValueError("No profile fields provided to update")

    r = client.put("/api/users/me", json=payload)
    r.raise_for_status()

    return Me(r.json())

