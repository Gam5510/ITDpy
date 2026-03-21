# 43_base_list_usage.py
# BaseList-подобное поведение на реальных ответах

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

posts = client.posts.list(limit=5)

print(len(posts))
print(posts.first())
print(posts.to_list())

for post in posts:
    print(post.id)

client.close()
