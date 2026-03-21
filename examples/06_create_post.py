# 06_create_post.py
# Создать обычный пост

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

post = client.posts.create(content="Привет из itdpy")

print(post.id)
print(post.content)
print(post.to_dict())
print(post)
client.close()
