# Модель Comment

## Пример

```python
comment = client.comments.create("POST_ID", content="Мой комментарий")

print(comment.id)
print(comment.content)
print(comment.likes_count)
print(comment.author.username if comment.author else None)
print(comment.to_json())
```

## Особенности

- `post_id` может быть `None`, если сервер его не прислал
- список комментариев приходит как `CommentsList`
- `CommentsList` поддерживает `next_cursor`, `has_more`, `total`

## CommentUpdate

```python
updated = client.comments.update("COMMENT_ID", "Новый текст")
print(updated.updated_at)
```
