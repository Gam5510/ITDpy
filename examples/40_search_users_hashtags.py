# 40_search_users_hashtags.py
# Поиск отдельно пользователей и хэштегов

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

users = client.search.users("gam55", limit=10)
hashtags = client.search.hashtags("python", limit=10)

print("users:", len(users))
print("hashtags:", len(hashtags))

for user in users:
    print(f"@{user.username}")

for hashtag in hashtags:
    print(f"#{hashtag.get('name')}")

client.close()
