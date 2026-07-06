
# ITDpy
## Модель Posts

### Пример ответа Posts
```json
  "data": {
        "posts": [
        {
	        Информация о 1 посте 
        },
         {
	        Информация о 2 посте
        },
         {
	        Информация о 3 посте
        }, 
        ],
        "pagination": {
            "limit": 20,
            "nextCursor": "2",
            "hasMore": false
        }
```
Информация о 1 посте размещена по структуре [Post](post.md), в конце размещена пагинация. Посты можно доставать так posts[0] информация о 1 посте.
### Поля 
| Поле | Тип | 
|------|-----|
|data.users|list[users]|
|data.pagination|[Pagination](pagination.md)|

## Пример 
```python
posts = client.posts.list()

print("Всего получено:", len(posts))
print("Есть ещё посты:", posts.pagination.has_more)
print("Next cursor:", posts.pagination.next_cursor)

for post in posts:
    print("\n--- Пост ---")
    print("ID:", post.id)
    print("Текст:", post.content)
    print("Лайки:", post.likes_count)
    print("Комментарии:", post.comments_count)
    print("Просмотры:", post.views_count)
    print("Закреплён:", post.is_pinned)
    print("Дата создания:", post.created_at)

    if post.author:
        print("Автор:", post.author.username)
```

← [Назад к документации](../index.md)