# 03_posts_feed.py
# Лента постов + list-like API

from itdpy import ITDClient, PostsTab

client = ITDClient(refresh_token="токен")

posts = client.posts.list(limit=10, tab=PostsTab.POPULAR)

print(len(posts))
print(posts.first())

for post in posts:
    print(post.id, post.content, post.likes_count)

if len(posts) > 0:
    first_post = posts[0]
    print(first_post["id"])
    print(first_post.to_dict())

client.close()
