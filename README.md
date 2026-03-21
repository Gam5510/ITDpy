# ITDpy

<p align="center">
  <img src="https://i.postimg.cc/gJ9z8RDk/ITDpy-(1)-pixian-ai.png" width="700">
</p>

![PyPI version](https://img.shields.io/pypi/v/itdpy)
![Downloads](https://static.pepy.tech/badge/itdpy)
![License](https://img.shields.io/github/license/Gam5510/ITDpy)

Python SDK для социальной сети итд.com.

> ⚠️ Неофициальный API-клиент.  
> SDK предназначен для разработки клиентских приложений и тестирования API в рамках действующих правил платформы.

## Установка

```bash
pip install itdpy
```

### Через git

```bash
git clone https://github.com/Gam5510/ITDpy
cd itdpy
pip install -r requirements.txt
pip install -e .
```

## Документация

[![Docs](https://img.shields.io/badge/docs-online-blue)](https://gam5510.github.io/ITDpy/)

## Быстрый старт

> ![Получение токена](https://i.ibb.co/DH1m8GL7/Assistant.png)
> Как получить токен

```python
from itdpy.client import ITDClient

client = ITDClient(refresh_token="Ваш refresh token")

me = client.users.me()
print(me.id)
print(me.username)
```
## Новые функции 1.x версии библиотеки 

### Модели как объект, dict и JSON сразу

```python
post = client.posts.get("POST_ID")

print(post.id)
print(post["createdAt"])
print(post.get("created_at"))
print(post.to_dict())
print(post.to_json())
```

### Списки как list-like объекты

```python
posts = client.posts.list(limit=10)

print(len(posts))
print(posts[0].id)
print(posts.first())
print(posts.to_json())
```

### Вложенные списки тоже умеют `to_json()`

```python
result = client.search.all("python")

print(result.users.to_json())
print(result.hashtags.to_json())
```

### PollBuilder

```python
from itdpy.models import PollBuilder

poll = PollBuilder("Как подавать котлеты?").add("С пюрешкой").add("Без пюрешки").multiple_choice(True).build()

post = client.posts.create(
    content="Голосуем",
    poll=poll,
)
```

### Poll можно сериализовать и как модель, и как payload

```python
print(poll.to_dict())
print(poll.to_json())
print(poll.to_request_dict())
```

### Markdown и HTML парсинг

```python
client.posts.create(
    content="**Жирный** текст",
    parse_md=True,
)

client.posts.create(
    content="<b>Жирный</b> текст",
    parse_html=True,
)
```

### Sync SSE streaming

```python
stream = client.notifications.stream()

@stream.on("notification")
def on_notification(event):
    print(event.data)

stream.run()
```

### Фильтрация событий по типу

```python
from itdpy.models import NotificationType

@stream.on("notification", type=NotificationType.LIKE)
def on_like(event):
    print(event.data)
```

### keep_online

```python
client.keep_online(
    on_event=lambda event_type, data: print(event_type, data),
    background=True,
)
```

### Enums вместо строк

```python
from itdpy import PostsTab, UserPostSorting, AccessType

posts = client.posts.list(tab=PostsTab.POPULAR)
user_posts = client.posts.get_user_posts("username", sort=UserPostSorting.NEW)
client.users.update_privacy(wall_access=AccessType.FOLLOWERS)
```

### Ошибки разделены по типам

```python
from itdpy import NotFoundError, ValidationError, RateLimitError, APIError

try:
    client.posts.get("invalid")
except NotFoundError:
    print("Не найдено")
except ValidationError as e:
    print(e.message)
except RateLimitError as e:
    print(e.retry_after)
except APIError as e:
    print(e.message)
```

### Пагинация батчами

```python
all_posts = client.posts.list_all(limit=100)
all_comments = client.comments.list_all("POST_ID", limit=100)
all_notifications = client.notifications.list_all(limit=100)
```

### Пост на чужую стену

```python
post = client.posts.post_to_wall(
    username="username",
    content="Привет на стену",
)
```

### После `close()` запросы больше не идут

```python
client.close()
client.posts.list()# -> RuntimeError
```

## Прочее

Проект активно развивается.
Если у вас есть идеи или предложения, создавайте issue или pull request.
Мой телеграм [@gam5510](https://t.me/gam5510) для обратной связи.