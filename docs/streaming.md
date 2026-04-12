# Streaming

`itdpy` поддерживает sync SSE streaming для уведомлений.

## Итерация через `for`

```python
for event in client.notifications.stream():
    print(event.event, event.data)
```

## Callback стиль

```python
stream = client.notifications.stream()

@stream.on("connected")
def on_connected(event):
    print("Connected!", event.data)

@stream.on("notification")
def on_notification(event):
    print("Got notification:", event.data)

@stream.on("reconnecting")
def on_reconnecting(event):
    delay = event.data.get("delay")
    print(f"Reconnecting in {delay}s (token refreshed automatically)")

@stream.on("error")
def on_error(event):
    print(f"Error: {event.data.get('message')}")

stream.run()
```

## Фильтрация по типу уведомления

```python
from itdpy.models import NotificationType

@stream.on("notification", type=NotificationType.LIKE)
def on_like(event):
    print(event.data)
```

Доступные значения `NotificationType`: `LIKE`, `COMMENT`, `REPLY`, `REPOST`, `FOLLOW`, `WALL_POST`.

## Остановка

```python
stream.stop()
```

## keep_online

```python
client.keep_online(
    on_event=lambda event_type, data: print(event_type, data),
    background=True,
)
```

## События Stream

| Событие | Описание | Данные |
|---------|---------|--------|
| `connected` | Успешное подключение | `ConnectedEventData` (user_id, timestamp) |
| `notification` | Новое уведомление | `Notification` (type, actor, preview) |
| `reconnecting` | Переподключение | `{"delay": int}` (секунды до переподключения) |
| `error` | Ошибка | `{"message": str}` |