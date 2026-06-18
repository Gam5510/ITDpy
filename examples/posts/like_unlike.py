"""Example: like and unlike a post."""
from itdpy import ITDClient

POST_ID = "REPLACE_WITH_POST_UUID"
with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    res = client.posts.like(POST_ID)
    print(f"Likes after like: {res.likes_count}")
    res = client.posts.unlike(POST_ID)
    print(f"Likes after unlike: {res.likes_count}")
