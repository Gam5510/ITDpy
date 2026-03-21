# 25_users_get.py
# Получить пользователя

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

user = client.users.get("gam5510")

print(user)
print(user.id)
print(user.username)
print(user.get("display_name"))
print(user["followers_count"])

client.close()
