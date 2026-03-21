# 11_update_post.py
# Обновить пост

from itdpy import ITDClient

client = ITDClient(refresh_token="Токен")

updated = client.posts.update(
    "a5acc9c9-d0c6-48b2-8b81-f351e249ab48",
    content="**Обновленный текст**",
    parse_md=True
)

print(updated.id)
print(updated.content)
print(updated.updated_at)

client.close()
