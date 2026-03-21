# 26_users_lists.py
# Подписчики / подписки

from itdpy import ITDClient

client = ITDClient(refresh_token="token")

followers = client.users.get_followers(user_id="c44d69c2-d35a-4ec0-8128-8e59e41053ba", limit=25, page=1) # Пагинация и страницы игнорируюется если это не ваш аккаунт 
following = client.users.get_following(user_id="7e06d23b-3db6-48ea-92e6-a6303c3870b1", limit=25, page=1)

print("followers:", len(followers))
print("following:", len(following))

client.close()
