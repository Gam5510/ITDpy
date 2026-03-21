# 21_delete_post.py
# Удалить пост

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

client.posts.delete("1d11a5e1-6ca3-4607-bf26-c798a5409d93")

client.close()
