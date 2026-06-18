"""Example: read and update privacy settings."""
from itdpy import ITDClient, AccessType

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    privacy = client.users.get_privacy()
    print(f"Private: {privacy.is_private}, Wall: {privacy.wall_access}")

    updated = client.users.update_privacy(
        is_private=False,
        wall_access=AccessType.FOLLOWERS,
    )
    print(f"Updated wall_access: {updated.wall_access}")
