# Notifications API

## Получить уведомления

```python
notifications = client.notifications.list(limit=20)
print(notifications.to_json())
```

## Получить все уведомления

Если `limit=None`, SDK забирает всё батчами по `50`.

```python
all_notifications = client.notifications.list_all()
limited_notifications = client.notifications.list_all(limit=120)
```

## Отметить уведомление прочитанным

```python
client.notifications.mark_read("NOTIFICATION_ID")
```

Если id невалидный, SDK выбросит `ValidationError`.  
Если id валидный, но сервер не находит уведомление, SDK преобразует ошибку в `NotFoundError`.

## Отметить все уведомления прочитанными

```python
client.notifications.mark_all_read()
```

## Streaming

```python
stream = client.notifications.stream()

@stream.on("notification")
def on_notification(event):
    print(event.data)

stream.run()
```
