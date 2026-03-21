# 24_comment_create_update_reply_delete.py
# Полный цикл комментария
from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

comment = client.comments.create(post_id="c44699ff-56a9-4b7a-875e-dc7612efbbb2", content="Мой комментарий")
print(comment.id, comment.content)

updated = client.comments.update(
    comment.id,
    "Обновленный комментарий",
)
print(updated.id, updated.updated_at)

reply = client.comments.reply(comment.id, content="Ответ")
print(reply.id, reply.content)

client.comments.like(comment["id"])
client.comments.unlike(comment.id)

client.comments.delete(reply.id)
client.comments.delete(comment.id)

client.close()
