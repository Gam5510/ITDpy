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
