"""Example: update profile fields."""
from itdpy import ITDClient

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    updated = client.users.update_profile(
        display_name="New Display Name",
        bio="Updated bio via ITDpy",
    )
    print(f"Updated profile: {updated.display_name}, bio: {updated.bio}")
