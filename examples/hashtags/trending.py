"""Example: get trending hashtags."""
from itdpy import ITDClient

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    trending = client.hashtags.trending(limit=10)
    for tag in trending:
        print(f"  #{tag.name} — {tag.posts_count} posts")
