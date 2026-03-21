# Comments API

## Получить комментарии поста

```python
from itdpy import CommentSort

comments = client.comments.list(
    "POST_ID",
    limit=20,
    sort=CommentSort.POPULAR,
)

print(comments.to_json())
```

## Получить все комментарии

`list_all()` идёт по курсору и забирает комментарии батчами по `50`.

```python
comments = client.comments.list_all("POST_ID", limit=100)
print(len(comments))
```

## Создать комментарий

```python
comment = client.comments.create("POST_ID", content="Мой комментарий")
print(comment.id, comment.content)
```

## Ответить на комментарий

```python
reply = client.comments.reply("COMMENT_ID", content="Ответ")
print(reply.id)
```

## Обновить комментарий

```python
updated = client.comments.update("COMMENT_ID", "Обновлённый текст")
print(updated.updated_at)
```

## Лайк / анлайк / удаление

```python
client.comments.like("COMMENT_ID")
client.comments.unlike("COMMENT_ID")
client.comments.delete("COMMENT_ID")
```
