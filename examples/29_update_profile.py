# 29_update_profile.py
# Обновить профиль

from itdpy import ITDClient
import random

client = ITDClient(refresh_token="токен")

me = client.users.me()

user = client.users.update_profile(
    display_name=f"{me.display_name} | {random.randint(10, 99)}",
    bio=f"{me.bio}!!!",
)

print(user.id)
print(user.display_name)
print(user.bio)

client.close()
