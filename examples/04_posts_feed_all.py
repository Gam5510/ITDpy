# 04_posts_feed_all.py
# Выгрузить весь feed через cursor

from itdpy import ITDClient, PostsTab

client = ITDClient(refresh_token="токен")

all_posts = client.posts.list_all(limit=50, tab=PostsTab.POPULAR)

print(len(all_posts))
for post in all_posts:
    print(post.id, post.created_at)

client.close()
