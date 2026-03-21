# 05_post_get.py
# Получить один пост

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

post = client.posts.get("23dd9026-133e-4437-9ab7-c69919626009")
print(post)
print(post.id)
print(post["content"])
print(post.views_count)

if post.author:
    print(post.author.username)
    print(post.author.display_name)

client.close()
