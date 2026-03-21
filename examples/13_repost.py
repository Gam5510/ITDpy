# 13_repost.py
# Репост поста

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

post = client.posts.repost("868a05e6-fddd-479d-9027-4f13f9b75007", content="Мой тестовый репост из itdpy")

print(post.id)
print(post.content)

client.close()
