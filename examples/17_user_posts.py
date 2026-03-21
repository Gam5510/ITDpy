# 17_user_posts.py
# Посты пользователя

from itdpy import ITDClient, UserPostSorting

client = ITDClient(refresh_token="токен")

posts = client.posts.get_user_posts(
    "gam5510",
    limit=20,
    sort=UserPostSorting.NEW,
)

print(len(posts))
for post in posts:
    print(post.id, post.get("content"))

client.close()
