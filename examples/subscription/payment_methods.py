"""Example: list payment methods."""
from itdpy import ITDClient

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    methods = client.subscription.get_payment_methods()
    for m in methods:
        default = " [DEFAULT]" if m.is_default else ""
        print(f"  {m.brand} *{m.last_four}{default} expires {m.expires_at}")
