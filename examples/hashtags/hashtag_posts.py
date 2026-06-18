"""Example: get posts for a hashtag."""
from itdpy import ITDClient

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    result = client.hashtags.get_posts("python", limit=20)
    print(f"Hashtag: #{result.hashtag.name}, posts: {len(result)}")
    for p in result.posts:
        print(f"  {p.id}: {(p.content or '')[:60]}")
