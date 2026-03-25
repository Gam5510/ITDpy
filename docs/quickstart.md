# Быстрый старт

## Установка

```bash
pip install itdpy
```

## Как получить refresh token

> ![Получение токена](https://i.ibb.co/DH1m8GL7/Assistant.png)
> Как получить токен

- Открой `итд.com` в браузере и войди в аккаунт.
- Открой DevTools.
- Перейди в `Application` -> `Cookies`.
- Найди cookie `refresh_token`.
- Скопируй её значение.

## Инициализация клиента

```python
from itdpy import ITDClient

client = ITDClient(refresh_token="YOUR_REFRESH_TOKEN")
```

## Config

```python
from itdpy import Config, ITDClient

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

Подробное описание всех параметров:

- [Config](config.md)

## Service name

```python
from itdpy import Config, ITDClient

config = Config(
    service="my_app",
    use_user_data_in_user_agent=True,
)

client = ITDClient(
    refresh_token="YOUR_REFRESH_TOKEN",
    config=config,
)
```

## Получить свой профиль

```python
me = client.users.me()

print(me.id)
print(me.username)
print(me.to_json())
```

## Получить ленту

```python
from itdpy import PostsTab

posts = client.posts.list(limit=10, tab=PostsTab.POPULAR)

for post in posts:
    print(post.id, post.content)
```

## Создать пост

```python
post = client.posts.create(content="Привет из itdpy")
print(post.id)
```

## Закрыть клиент

```python
client.close()
```
