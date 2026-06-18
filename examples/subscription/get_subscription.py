"""Example: get subscription info."""
from itdpy import ITDClient

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    sub = client.subscription.get()
    print(f"Status: {sub.status}, active: {sub.is_active}")
    print(f"Expires: {sub.expires_at}, auto-renewal: {sub.auto_renewal}")
