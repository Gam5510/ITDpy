# Модель Post

## Что содержит `Post`

- основные поля поста
- автора
- attachments
- poll
- original post
- wall recipient

## Пример

```python
post = client.posts.get("POST_ID")

print(post.id)
print(post.content)
print(post.likes_count)
print(post.author.username if post.author else None)
print(post.to_json())
```

## Особенности

- работает как объект: `post.id`
- работает как dict: `post["createdAt"]`
- работает как JSON: `post.to_json()`
- вложенные списки тоже list-like: `post.attachments.to_json()`

## Poll внутри поста

```python
if post.poll:
    print(post.poll.question)
    print(post.poll.options.to_json())
```

## Обновление поста

При вызове:

```python
updated = client.posts.update("POST_ID", content="Новый текст")
```

SDK возвращает `PostUpdate`, где доступны как минимум:

```python
print(updated.id)
print(updated.content)
print(updated.updated_at)
```
