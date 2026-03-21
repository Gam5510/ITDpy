# 18_user_posts_all.py
# Все посты пользователя через cursor

from itdpy import ITDClient, UserPostSorting

client = ITDClient(refresh_token="токен")

posts = client.posts.get_all_user_posts(
    "gam5510",
    limit=50,
    sort=UserPostSorting.NEW,
)

print(len(posts))
print(posts.first())

client.close()
