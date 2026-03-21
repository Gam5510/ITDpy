# 02_me.py
# Получение своего профиля и работа с моделью как с объектом/dict/json

from itdpy import ITDClient

client = ITDClient(refresh_token="token")

me = client.users.me()

print(me.id)
print(me.username)
print(me["displayName"])
print(me.to_dict())
print(me.to_json())

client.close()
