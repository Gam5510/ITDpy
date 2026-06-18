"""Example: get own profile."""
from itdpy import ITDClient

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    me = client.users.me()
    print(f"Logged in as: @{me.username} ({me.display_name})")
    print(f"Followers: {me.followers_count}, Following: {me.following_count}")
