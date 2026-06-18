"""Example: list posts from the global feed."""
from itdpy import ITDClient, PostsTab

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    feed = client.posts.list(limit=20, tab=PostsTab.POPULAR)
    print(f"Fetched {len(feed)} posts (has_more={feed.has_more})")
    for post in feed:
        author = post.author.username if post.author else "?"
        print(f"  [{post.id}] {author}: {(post.content or '')[:60]}")
