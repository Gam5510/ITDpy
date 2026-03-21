# 01_init.py
# Базовая инициализация клиента

from itdpy import ITDClient

client = ITDClient(refresh_token="token")

print(client.access_token)
print(client.user_id)

client.close()
