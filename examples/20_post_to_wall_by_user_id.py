# 20_post_to_wall_by_user_id.py
# Написать на стену по user_id

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

post = client.posts.post_to_wall(
    user_id="832b4623-3563-4a53-b4dc-abac02a4c243",
    content="Привет на стену по id",
)

print(post.id)
print(post.wall_recipient_id)

client.close()
