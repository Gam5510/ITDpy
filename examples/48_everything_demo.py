# 48_everything_demo.py
# Большой комбинированный пример

from itdpy import ITDClient, PostsTab
from itdpy.models import Poll, PollBuilder

client = ITDClient(refresh_token="токен")

me = client.users.me()
print("me:", me.get("username"))

feed = client.posts.list(limit=3, tab=PostsTab.POPULAR)
print("feed size:", len(feed))

new_post = client.posts.create(
    content="Демо пост с моделью Poll",
    poll=Poll(
        question="Выбери вариант",
        options=["A", "B", "C", "D"],
        multipleChoice=True
    ),
)
print("created:", new_post.id)

list = ["A", "B", "C", "D"]
poll_builder = PollBuilder(question="Выбери вариант")

for item in list:
    poll_builder.add(item)

poll_builder.multiple_choice(True)
poll_builder.build()

new_post = client.posts.create(
    content="Демо пост с Poll Builder ",
    poll=poll_builder
)
print("created:", new_post.id)

liked = client.posts.like(new_post.id)
print("likes:", liked.likes_count)

comments = client.comments.list(new_post.id, limit=10)
print("comments:", len(comments))

comment = client.comments.create(new_post.id, content="Первый комментарий")
print("comment:", comment.id)

notifications = client.notifications.list(limit=5)
print("notifications:", len(notifications))

portal = client.discovery.portal()
print("portal:", portal.title, portal.url)

client.posts.view(new_post.id)
client.posts.delete(new_post.id)

client.close()
