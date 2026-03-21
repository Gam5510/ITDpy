# Users API

## Получить себя и пользователя

```python
me = client.users.me()
user = client.users.get("username")
```

## Подписаться / отписаться

```python
client.users.follow("username")
client.users.unfollow("username")
```

## Подписчики и подписки

```python
followers = client.users.get_followers("USER_ID", limit=25, page=1)
following = client.users.get_following("USER_ID", limit=25, page=1)

print(followers.to_json())
```

## Follow status списком

```python
statuses = client.users.follow_status([
    "USER_ID_1",
    "USER_ID_2",
])

for item in statuses:
    print(item.id, item.is_following)
```

## Обновить профиль

```python
user = client.users.update_profile(
    display_name="Новое имя",
    bio="Новая bio",
)
```

## Приватность

```python
from itdpy import AccessType

privacy = client.users.update_privacy(
    is_private=True,
    wall_access=AccessType.FOLLOWERS,
    likes_visibility=AccessType.EVERYONE,
    show_last_seen=False,
)
```

## Настройки уведомлений

```python
settings = client.users.update_notification_settings(
    enabled=True,
    comments=True,
    follows=True,
    likes=True,
    mentions=True,
    sound=True,
    wall_posts=True,
)
```

## Block / unblock

```python
client.users.block("username")
client.users.unblock("username")
```
