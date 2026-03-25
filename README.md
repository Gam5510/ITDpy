# ITDpy

<p align="center">
  <img src="https://i.postimg.cc/gJ9z8RDk/ITDpy-(1)-pixian-ai.png" width="700">
</p>

![PyPI version](https://img.shields.io/pypi/v/itdpy?nocache=1)
![Downloads](https://static.pepy.tech/badge/itdpy?nocache=1)
![License](https://img.shields.io/github/license/Gam5510/ITDpy)
[![Docs](https://img.shields.io/badge/docs-online-blue)](https://gam5510.github.io/ITDpy/)

Python SDK для социальной сети итд.com.

> Неофициальный API-клиент.
> SDK предназначен для клиентских приложений, интеграций и сервисов, работающих в рамках правил платформы.

## Безопасность и позиция проекта

ITDpy не поддерживает спам, массовую автоматизацию, накрутку, ботов для злоупотреблений и другие сценарии, нарушающие правила платформы.

Библиотека ориентирована на:

- клиентские приложения
- внутренние сервисы
- интеграции
- тестирование API

## User-Agent

По умолчанию библиотека использует такой `User-Agent`:

```text
Mozilla/5.0 (Linux; Android 10; K) 
AppleWebKit/537.36 (KHTML, like Gecko) 
Chrome/122.0.0.0 Mobile Safari/537.36
```

Это вынужденная мера совместимости. На практике API refresh-аутентификации может не работать с дефолтным `itdpy/...` и сервер начинает воспринимать такой запрос как бот.

Поэтому стартовый `User-Agent` в ITDpy намеренно задан как браузерный профиль, чтобы библиотека работала стабильно.

Важно:

- это сделано не для обхода правил платформы
- это сделано для совместимости с API, которое без этого нестабильно или не работает
- проект не поддерживает спам-ботов и абьюз API
- проект поддерживает только нормальные сервисные и клиентские сценарии использования

## Установка

```bash
pip install itdpy
```

### Через git

```bash
git clone https://github.com/Gam5510/ITDpy
cd ITDpy
pip install -r requirements.txt
pip install -e .
```

## Документация

[![Docs](https://img.shields.io/badge/docs-online-blue)](https://gam5510.github.io/ITDpy/)

## Быстрый старт

> ![Получение токена](https://i.ibb.co/DH1m8GL7/Assistant.png)
> Как получить токен

- Открой `итд.com` в браузере и войди в аккаунт.
- Открой DevTools (F12).
- Перейди в `Application` -> `Cookies`.
- Найди cookie `refresh_token`.
- Скопируй её значение.

```python
from itdpy import ITDClient

client = ITDClient(refresh_token="YOUR_REFRESH_TOKEN")

me = client.users.me()
print(me.id)
print(me.username)
```

## Конфигурация

```python
from itdpy import ITDClient, Config

config = Config(
    timeout=30,
    upload_timeout=180,
    max_retries=5,
    backoff_factor=2.0,
)

client = ITDClient(
    refresh_token="YOUR_REFRESH_TOKEN",
    config=config,
)
```

## Кастомный User-Agent

Если нужен полностью свой `User-Agent`, можно передать его через `Config.custom_user_agent`:

```python
from itdpy import ITDClient, Config

config = Config(
    custom_user_agent="my-app/2.0",
)

client = ITDClient(
    refresh_token="YOUR_REFRESH_TOKEN",
    config=config,
)
```

Если `custom_user_agent` не задан, библиотека использует стандартный стартовый браузерный `User-Agent`.

## User-Agent с данными пользователя

Если нужно после авторизации переключиться на `User-Agent` с данными SDK и пользователя, включи `use_user_data_in_user_agent=True`:

```python
from itdpy import ITDClient, Config

config = Config(
    service="my_app",
    use_user_data_in_user_agent=True,
)

client = ITDClient(
    refresh_token="YOUR_REFRESH_TOKEN",
    config=config,
)
```

По умолчанию этот режим выключен.

Шаблон можно переопределить через `Config.user_agent_template`:

```python
from itdpy import Config

config = Config(
    use_user_data_in_user_agent=True,
    user_agent_template="itdpy/{sdk_version} ({parts})",
)
```

Доступные поля шаблона:

- `{sdk_version}`
- `{parts}`
- `{user_id}`
- `{service}`

## Примеры

### Получить пост

```python
post = client.posts.get("POST_ID")
print(post.id)
print(post.to_dict())
```

### Лента постов

```python
posts = client.posts.list(limit=10)
print(len(posts))
print(posts[0].id)
```

### Создать пост

```python
client.posts.create(
    content="Привет из ITDpy",
)
```

### Markdown и HTML

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

### SSE streaming

```python
stream = client.notifications.stream()

@stream.on("notification")
def on_notification(event):
    print(event.data)

stream.run()
```

### keep_online

```python
client.keep_online(
    on_event=lambda event_type, data: print(event_type, data),
    background=True,
)
```

### Обработка ошибок

```python
from itdpy import APIError, NotFoundError, RateLimitError, ValidationError

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

## Прочее

Проект активно развивается. Если у вас есть предложения или pull request, создавайте issue в репозитории.
Мой телеграм для обратной связи: [@gam5510](https://t.me/gam5510)
