# 14_view_post.py
# Отметить пост просмотренным

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

result = client.posts.view("868a05e6-fddd-479d-9027-4f13f9b75007")
print(result.viewed)

client.close()
