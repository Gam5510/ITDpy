# Poll Model

## `Poll`

Модель опроса, которая приходит из API и может использоваться для создания нового poll.

### Поля

| Поле | Тип |
|---|---|
| `id` | `str | None` |
| `post_id` | `str | None` |
| `question` | `str` |
| `options` | `BaseList[PollOption]` |
| `total_votes` | `int` |
| `has_voted` | `bool` |
| `voted_option_ids` | `BaseList[str]` |
| `multiple_choice` | `bool` |
| `created_at` | `str | None` |

### Пример ответа API

```json
{
  "id": "068ef603-9cc8-4a83-ab57-82152b173fd7",
  "postId": "a90b001d-c7d3-497f-ba23-bb30b03d3891",
  "question": "Как ваши дела?",
  "multipleChoice": false,
  "options": [
    {
      "id": "e2dc014d-4ec2-4cdf-b65c-0430ab73e5c8",
      "text": "классно",
      "position": 0,
      "votesCount": 0
    },
    {
      "id": "6f96247d-c097-43ce-941c-651d441387c3",
      "text": "хорошо",
      "position": 1,
      "votesCount": 1
    }
  ],
  "totalVotes": 1,
  "hasVoted": true,
  "votedOptionIds": [
    "6f96247d-c097-43ce-941c-651d441387c3"
  ],
  "createdAt": "2026-03-20T13:25:59.248Z"
}
```

### Пример использования

```python
if post.poll:
    print(post.poll.question)
    print(post.poll["multipleChoice"])
    print(post.poll.options.to_json())

    for option in post.poll.options:
        print(option.id, option.text, option.votes_count)
```

### Методы

#### `to_dict()`

Полная сериализация модели.

```python
print(post.poll.to_dict())
```

#### `to_json()`

```python
print(post.poll.to_json())
```

#### `to_request_dict()`

Payload для создания опроса через API.

```python
print(post.poll.to_request_dict())
```

#### `get()` и `__getitem__`

```python
print(post.poll.get("question"))
print(post.poll["question"])
print(post.poll["multipleChoice"])
```

## `PollOption`

### Поля

| Поле | Тип |
|---|---|
| `id` | `str | None` |
| `text` | `str` |
| `position` | `int` |
| `votes_count` | `int` |

## `PollBuilder`

Удобный builder для пошагового создания опроса.

### Пример

```python
from itdpy.models import PollBuilder

poll = (
    PollBuilder("Как подавать котлеты?")
    .add("С пюрешкой")
    .add("Без пюрешки")
    .multiple_choice(True)
)
```

### Методы

| Метод | Описание |
|---|---|
| `add(value)` | Добавляет вариант ответа |
| `multiple_choice(flag)` | Включает множественный выбор |
| `build()` | Возвращает `Poll` |
| `to_dict()` | Возвращает полную модель `Poll` |
| `to_json()` | JSON-строка |
| `to_request_dict()` | Payload для API |
| `get()` | Получение поля как у dict |

### Особенности

- `add()` принимает не только `str`, но и числа, которые автоматически превращаются в строку
- `PollBuilder` можно передавать напрямую в `client.posts.create(..., poll=...)`
- `build()` нужен только если ты хочешь получить именно объект `Poll`

### Пример с числами

```python
poll = PollBuilder("Какая цифра лучше?").add(1).add(2).add(3)

print(poll.to_dict())
print(poll.to_request_dict())
```

## См. также

- [Polls API Usage](../polls.md)
- [Post Model](post.md)
