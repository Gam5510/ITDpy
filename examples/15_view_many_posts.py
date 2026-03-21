# 15_view_many_posts.py
# Отметить несколько постов просмотренными

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

result = client.posts.view_many(["0aae8a5e-dfcc-4298-b120-f534288db1d5", "2a46e131-6a92-4c1a-9fb8-58aaf7f3e4e0", "28cae55b-4fbb-49f5-8f8b-fa23690d95a8"])
print(result)

client.close()
