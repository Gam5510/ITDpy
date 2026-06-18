"""Example: get platform app versions."""
from itdpy import ITDClient

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    apps = client.platform.get_apps()
    for name, app in apps.items():
        print(f"  {name}: {app}")
