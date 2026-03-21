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
    print(event.data)

@stream.on("notification")
def on_notification(event):
    print(event.data)

stream.run()
```

## Фильтрация по типу уведомления

```python
from itdpy.models import NotificationType

@stream.on("notification", type=NotificationType.LIKE)
def on_like(event):
    print(event.data)
```

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

## Что умеет stream

- sync loop
- callbacks
- авто-реконнект
- exponential backoff
- игнор `ping`
- парсинг `connected` и `notification`
