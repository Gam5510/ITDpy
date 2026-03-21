# 44_closed_client_guard.py
# После close запросы больше не должны идти, если не пересоздать клиента

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")
client.close()

try:
    client.posts.list()
except RuntimeError as e:
    print("OK:", e)
