# 10_create_post_with_poll.py
# Создать пост с Poll моделью

from itdpy import ITDClient
from itdpy.models import Poll

client = ITDClient(refresh_token="токен")

post = client.posts.create(
    content="**Голосование!**",
    poll=Poll(
        question="Как ваши дела?",
        options=["классно", "хорошо", "нормально", "плохо"],
    ),
    parse_md=True
)

print(post.id)
print(post.poll)
print(post["poll"])

client.close()
