"""Example: list comments on a post."""
from itdpy import ITDClient, CommentSort

POST_ID = "REPLACE_WITH_POST_UUID"
with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    comments = client.comments.list(POST_ID, limit=20, sort=CommentSort.NEWEST)
    print(f"Comments: {len(comments)}, has_more={comments.has_more}")
    for c in comments:
        print(f"  @{c.author.username if c.author else '?'}: {c.content[:60]}")
