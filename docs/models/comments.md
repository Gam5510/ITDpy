# ITDpy

## Модель Comments

### Пример ответа Comments
```json
{
  "data": {
    "comments": [
      {
        1 коммент
        },
        "attachments": [],
        "replies": [
          {
          ответы
          }
        ]
      },
	  {
        2 коммент
		},
        "attachments": [],
        "replies": [
        ответы
				]
      }
    ],
    "pagination": {
      "limit": 20,
      "hasMore": false
    }
  }
}
```
### Поля объекта Comment

| Поле | Тип | 
|------|-----|
|data.comments|list[Comment]|
|data.pagination|[Pagination](pagination.md)|

### Пример использования
```python
comments  =  client.comments.list(post_id="6f14ee05-e0c5-4133-8f42-aca16bde154c")

for  comment  in  comments:
	print(comment.content)
	for  reply  in  comment.replies:
		print(" Автор: ",  reply.author.display_name)
		print(" Ответ:",  reply.content)
```

← [Назад к документации](../index.md)