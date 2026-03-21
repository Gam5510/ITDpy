# Модель Notification

## Пример

```python
notifications = client.notifications.list(limit=20)
notification = notifications.first()

print(notification.id)
print(notification.type)
print(notification.preview)
print(notification.actor.display_name)
```

## Поля

- `id`
- `type`
- `target_type`
- `target_id`
- `preview`
- `read_at`
- `created_at`
- `user_id`
- `actor`
- `read`
- `sound`

`user_id` может быть `None`, если сервер его не прислал.

## Типы уведомлений

Используется enum `NotificationType`:

- `LIKE`
- `COMMENT`
- `REPLY`
- `REPOST`
- `FOLLOW`
