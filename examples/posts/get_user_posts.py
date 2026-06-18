"""Example: get a user's posts with auto-pagination."""
from itdpy import ITDClient

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    posts = client.posts.get_all_user_posts("someusername", limit=50)
    print(f"Total posts fetched: {len(posts)}")
    for p in posts:
        print(f"  {p.created_at}: {(p.content or '')[:80]}")
