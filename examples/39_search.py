# 39_search.py
# Общий поиск

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

result = client.search.all("python")

print(result.users.to_json())
print(result.hashtags)
print(result)

client.close()
