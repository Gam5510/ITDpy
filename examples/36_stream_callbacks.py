# 36_stream_callbacks.py
# SSE stream через callbacks с автоматическим обновлением токена

from itdpy import ITDClient
from itdpy.models import Notification, NotificationType

client = ITDClient(refresh_token="token")
stream = client.notifications.stream()

# Токен автоматически обновляется при потере соединения
# и при получении 401 ошибки на любых запросах!


@stream.on("connected")
def on_connected(event):
    print("connected", event.data)


@stream.on("notification")
def on_notification(event):
    notification: Notification = event.data
    print("notification", notification.type, notification.preview)


@stream.on("notification", type=NotificationType.LIKE)
def on_like(event):
    notification: Notification = event.data
    print("LIKE from", notification.actor.username)


@stream.on("reconnecting")
def on_reconnect(event):
    delay = event.data.get("delay")
    print(f"Reconnecting in {delay}s... (Token automatically refreshed)")


@stream.on("error")
def on_error(event):
    print("Stream error:", event.data.get("message"))


stream.run()
