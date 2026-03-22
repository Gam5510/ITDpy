# Быстрый старт

## Установка

```bash
pip install itdpy
```
> ![Получение токена](https://i.ibb.co/DH1m8GL7/Assistant.png)
> Как получить токен

- Открой итд.com в браузере и войди в аккаунт
- Открой DevTools (F12) → Application → Cookies
- Найди куку refresh_token и скопируй значение

## Инициализация клиента

```python
from itdpy import ITDClient

client = ITDClient(refresh_token="YOUR_REFRESH_TOKEN")
```

## Config библиотеки

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

## Имя сервиса

```python
from itdpy import ITDClient, Config

config = Config(service="my_app")
client = ITDClient(
    refresh_token="YOUR_REFRESH_TOKEN",
    config=config,
)
```

SDK добавит `service=my_app` в `User-Agent`.

## Получить себя

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

## Закрыть клиента

```python
client.close()
```
