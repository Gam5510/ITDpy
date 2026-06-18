"""Example: follow and unfollow a user."""
from itdpy import ITDClient

TARGET = "someusername"
with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    client.users.follow(TARGET)
    print(f"Now following @{TARGET}")

    client.users.unfollow(TARGET)
    print(f"Unfollowed @{TARGET}")
