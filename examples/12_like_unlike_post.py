# 12_like_unlike_post.py
# Лайк / анлайк поста

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

liked = client.posts.like("a5acc9c9-d0c6-48b2-8b81-f351e249ab48")
print(liked.likes_count)
print(liked["likesCount"])

unliked = client.posts.unlike("a5acc9c9-d0c6-48b2-8b81-f351e249ab48")
print(unliked.likes_count)

client.close()
