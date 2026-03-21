# Polls

`Poll` и `PollBuilder` используются для создания и отправки опросов в `posts.create()` и `posts.post_to_wall()`.

## Быстрый старт

### Через `Poll`

```python
from itdpy.models import Poll

poll = Poll(
    question="Как подавать котлеты?",
    options=["С пюрешкой", "Без пюрешки"],
    multipleChoice=True,
)
```

### Через `PollBuilder`

```python
from itdpy.models import PollBuilder

poll = (
    PollBuilder("Как подавать котлеты?")
    .add("С пюрешкой")
    .add("Без пюрешки")
    .multiple_choice(True)
    .build()
)
```

## Отправка опроса

### Создать пост с опросом

```python
post = client.posts.create(
    content="Голосуем",
    poll=Poll(
        question="Как подавать котлеты?",
        options=["С пюрешкой", "Без пюрешки"],
        multipleChoice=True,
    ),
)
```

### Builder без `build()`

`PollBuilder` тоже поддерживает сериализацию, поэтому его можно передавать напрямую:

```python
post = client.posts.create(
    content="Голосуем",
    poll=(
        PollBuilder("Как подавать котлеты?")
        .add("С пюрешкой")
        .add("Без пюрешки")
        .multiple_choice(True)
    ),
)
```

### Пост на чужую стену

```python
post = client.posts.post_to_wall(
    username="username",
    content="Опрос на стену",
    poll=(
        PollBuilder("Что добавить в itdpy?")
        .add("Больше моделей")
        .add("Больше примеров")
        .add("Больше streaming")
        .multiple_choice(True)
    ),
)
```

## Сериализация

### `to_dict()`

Возвращает полную модель `Poll`.

```python
poll = Poll(
    question="Как ваши дела?",
    options=["Отлично", "Нормально", "Плохо"],
)

print(poll.to_dict())
```

Результат:

```python
{
    "question": "Как ваши дела?",
    "options": [
        {"text": "Отлично", "position": 0, "votesCount": 0},
        {"text": "Нормально", "position": 0, "votesCount": 0},
        {"text": "Плохо", "position": 0, "votesCount": 0},
    ],
    "totalVotes": 0,
    "hasVoted": False,
    "votedOptionIds": [],
    "multipleChoice": False,
}
```

### `to_request_dict()`

Возвращает payload для API.

```python
print(poll.to_request_dict())
```

Результат:

```python
{
    "question": "Как ваши дела?",
    "multipleChoice": False,
    "options": [
        {"text": "Отлично"},
        {"text": "Нормально"},
        {"text": "Плохо"},
    ],
}
```

### `to_json()`

```python
print(poll.to_json())
```

## Работа как с dict

И `Poll`, и `PollBuilder` поддерживают:

```python
print(poll["question"])
print(poll.get("multipleChoice"))
```

## Числовые варианты

`PollBuilder` автоматически приводит значения к строке:

```python
poll = PollBuilder("Какая цифра лучше?").add(1).add(2).add(3)

print(poll.to_request_dict())
```

## Голосование

```python
poll = client.posts.vote(
    post_id="POST_ID",
    option_ids="OPTION_ID",
)

print(poll.question)
print(poll.total_votes)
print(poll.options.to_json())
```

## См. также

- [Poll Model](models/poll.md)
- [Posts API](posts.md)
