"""Example: search users and hashtags."""
from itdpy import ITDClient

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    results = client.search.all("python", user_limit=5, hashtag_limit=5)
    print(f"Users: {[u.username for u in results.users]}")
    print(f"Hashtags: {[h.name for h in results.hashtags]}")
