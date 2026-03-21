# 22_comments.py
# Получить комментарии к посту

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

comments = client.comments.list("bac4ead9-8ecc-4c59-8217-1af1c7cf9198", limit=100)

print(len(comments))
for comment in comments:
    print(comment.id, comment.content, comment.likes_count)

client.close()
