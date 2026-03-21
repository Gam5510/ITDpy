# ITDpy

<p align="center">
  <img src="https://i.postimg.cc/gJ9z8RDk/ITDpy-(1)-pixian-ai.png" width="700">
</p>

![PyPI version](https://img.shields.io/pypi/v/itdpy?nocache=1)
![Downloads](https://static.pepy.tech/badge/itdpy?nocache=1)
![License](https://img.shields.io/github/license/Gam5510/ITDpy)

Python SDK для социальной сети итд.com.

Основные возможности:

- объектные Pydantic-модели
- dict-like и JSON-like доступ к данным
- list-like ответы для коллекций
- polling и `PollBuilder`
- sync SSE streaming
- типизированные enums
- нормальная классификация ошибок

## Быстрые ссылки

- [Быстрый старт](quickstart.md)
- [Обзор API](api.md)
- [Модели в SDK](models.md)
- [Streaming](streaming.md)
- [Polls](polls.md)

## Пример

```python
from itdpy import ITDClient, PostsTab

client = ITDClient(refresh_token="YOUR_REFRESH_TOKEN")

posts = client.posts.list(limit=10, tab=PostsTab.POPULAR)
print(len(posts))
print(posts.first())

client.close()
```

