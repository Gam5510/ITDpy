# 19_post_to_wall_by_username.py
# Написать на стену по username

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

post = client.posts.post_to_wall(
    username="irratium",
    content="Привет! тестовый **пост** на *стену*, через `itdpy`",
    parse_md=True
)

print(post.get("id"))
print(post.wall_recipient_id)
print(post["content"])
client.close()


