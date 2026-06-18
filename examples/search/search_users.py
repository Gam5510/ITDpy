"""Example: search only users."""
from itdpy import ITDClient

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    users = client.search.users("john", limit=10)
    for u in users:
        print(f"  @{u.username} — {u.display_name}")
