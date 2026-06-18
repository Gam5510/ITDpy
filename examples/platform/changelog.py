"""Example: get platform changelog."""
from itdpy import ITDClient

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    changelog = client.platform.get_changelog()
    print(f"Versions in changelog: {len(changelog)}")
    for v in changelog:
        print(f"  {v}")
