# ITDpy

## Модель Pagination

### Используется в моделях:
-   Posts
-   Comments
-   Users

### Поля

| Поле | Тип | Описание |
|--|--|--|
| page |int|Текущая страница|
|limit|int|Количество элементов|
| total|int|Общее количество|
|has_more|bool|Есть ли ещё страницы|

## Пример использования
```python
posts = client.posts.list()
if posts.pagination: 
	print(posts.pagination.page) 
	print(posts.pagination.total)
```

← [Назад к документации](../index.md)