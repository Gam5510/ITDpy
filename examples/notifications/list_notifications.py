"""Example: list notifications."""
from itdpy import ITDClient

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    notifs = client.notifications.list(limit=20)
    print(f"Notifications: {len(notifs)}, total={notifs.total}")
    for n in notifs:
        print(f"  [{n.type}] from @{n.actor.username}: {n.preview or ''}")
