# 23_comments_all.py
# Выгрузить все комментарии поста

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

comments = client.comments.list_all("c5391c81-9769-4c56-bf85-66e37c2d888f", limit=250)

print(len(comments))
print(comments.to_dict())

client.close()
