# Модели в itdpy

Начиная с текущей архитектуры SDK, `itdpy` использует единый подход к данным:

- API никогда не должен возвращать сырые `dict` как основной результат
- данные приходят как Pydantic-модели
- списки приходят как list-like объекты на базе `BaseList`
- модели можно использовать и как объект, и как словарь, и как JSON

## Что это значит на практике

Одна и та же сущность может использоваться в нескольких стилях одновременно.

### Как обычная Pydantic-модель

```python
post = client.posts.get("POST_ID")

print(post.id)
print(post.content)
print(post.author.username)
```

Здесь модель ведёт себя как обычный typed-объект с автодополнением IDE и строгими типами.

### Как словарь

```python
print(post["id"])
print(post["createdAt"])
print(post["created_at"])
print(post.get("wallRecipientId"))
```

Поддерживаются:

- Python-имена полей: `created_at`
- alias API: `createdAt`

## Универсальные методы моделей

Практически каждая модель в SDK поддерживает одинаковый интерфейс:

### `to_dict()`

Возвращает словарь с alias API.

```python
print(post.to_dict())
```

Пример:

```python
{
    "id": "POST_ID",
    "content": "Привет",
    "createdAt": "2026-03-21T10:00:00Z"
}
```

### `to_json()`

```python
print(post.to_json())
```

### `to_request_dict()`

Используется для сериализации в payload запроса.

Для большинства моделей это то же самое, что `to_dict()`.

Для специальных моделей, например `Poll`, это именно формат для API:

```python
poll.to_request_dict()
```

### `get()`

```python
print(post.get("id"))
print(post.get("createdAt"))
print(post.get("missing", None))
```

### `__getitem__`

```python
print(post["id"])
print(post["createdAt"])
```

### `__repr__` и `__str__`

```python
print(post)
print(repr(post))
```

`print(post)` даёт JSON-подобный вывод, удобный для отладки.  
`repr(post)` даёт короткий debug-view.

## Списковые модели

Списковые ответы в `itdpy` не являются сырыми `list`.  
Они являются list-like объектами на базе `BaseList`.

Например:

- `PostsList`
- `UsersList`
- `CommentsList`
- `NotificationsList`
- вложенные списки вроде `post.attachments`, `poll.options`, `result.users`

## Что умеет `BaseList`

### Итерация

```python
posts = client.posts.list(limit=10)

for post in posts:
    print(post.id)
```

### Индексация

```python
print(posts[0])
print(posts[0].id)
```

### Длина

```python
print(len(posts))
```

### Первый элемент

```python
print(posts.first())
```

### Сериализация

```python
print(posts.to_dict())
print(posts.to_json())
print(posts.to_request_dict())
```

### Доступ как список

```python
print(posts.get(0))
```

## Вложенные списки внутри моделей

Это важная часть DX.

Например:

```python
result = client.search.all("python")

print(result.users.to_json())
print(result.hashtags.to_dict())
print(result.users[0].username)
```

Или:

```python
post = client.posts.get("POST_ID")

print(post.attachments.to_json())
print(post.spans.to_dict())
```

Или:

```python
poll = client.posts.vote(post_id="POST_ID", option_ids="OPTION_ID")

print(poll.options.to_json())
print(poll.voted_option_ids.to_dict())
```

## Модели можно передавать обратно в API

Некоторые модели можно не только получать, но и использовать как входные данные.

Пример с `Poll`:

```python
from itdpy.models import Poll

poll = Poll(
    question="Как подавать котлеты?",
    options=["С пюрешкой", "Без пюрешки"],
    multipleChoice=True,
)

post = client.posts.create(
    content="Голосуем",
    poll=poll,
)
```

Пример с `PollBuilder`:

```python
from itdpy.models import PollBuilder

poll = (
    PollBuilder("Что добавить в itdpy?")
    .add("Больше моделей")
    .add("Больше примеров")
    .multiple_choice(True)
)

post = client.posts.create(
    content="Опрос",
    poll=poll,
)
```

## PollBuilder тоже ведёт себя как модель

Даже если это builder, он поддерживает:

```python
poll = PollBuilder("Какая цифра лучше?").add(1).add(2).add(3)

print(poll.to_dict())
print(poll.to_json())
print(poll.to_request_dict())
print(poll["question"])
print(poll.get("multipleChoice"))
```

То есть его можно использовать почти так же, как обычную модель.

## Зачем это сделано

Цель этой архитектуры:

- сохранить типобезопасность Pydantic
- не заставлять пользователя работать с сырыми словарями
- оставить удобство JSON-стиля
- сделать ответы API предсказуемыми
- упростить сериализацию обратно в API

## Кратко

В `itdpy` модель может быть:

- Pydantic-моделью
- объектом с атрибутами
- dict-like сущностью
- JSON-источником
- частью request payload

И всё это без ручной конвертации в каждом месте.
