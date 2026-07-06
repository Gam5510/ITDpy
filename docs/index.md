# ITDpy

<p align="center">
  <img src="https://i.postimg.cc/gJ9z8RDk/ITDpy-(1)-pixian-ai.png" width="700">
</p>

![PyPI version](https://img.shields.io/pypi/v/itdpy?nocache=1)
![Downloads](https://static.pepy.tech/badge/itdpy?nocache=1)
![License](https://img.shields.io/github/license/Gam5510/ITDpy)

Python SDK для итд.com API.

## Основные возможности

- объектные модели на Pydantic
- dict-like и JSON-like доступ к данным
- list-like ответы для коллекций
- PollBuilder
- sync SSE streaming
- enums
- нормальная типизация ошибок

## Быстрые ссылки

- [Быстрый старт](quickstart.md)
- [Config](config.md)
- [Обзор API](api.md)
- [Модели в SDK](models.md)
- [Streaming](streaming.md)
- [Polls](polls.md)

## Пример

Проще всего авторизоваться по email и паролю — SDK сам пройдёт через браузер
капчу Cloudflare Turnstile и получит токен доступа:

```python
from itdpy import ITDClient, PostsTab

client = ITDClient(email="user@example.com", password="my-password")

posts = client.posts.list(limit=10, tab=PostsTab.POPULAR)
print(len(posts))
print(posts.first())

client.close()
```

Как альтернативный вариант — если у вас уже есть сохранённый `refresh_token`
(например, из предыдущей сессии или для CI без браузера), его можно передать
напрямую:

```python
client = ITDClient(refresh_token="YOUR_REFRESH_TOKEN")
```
