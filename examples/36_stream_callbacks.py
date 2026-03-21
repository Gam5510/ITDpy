# 36_stream_callbacks.py
# SSE stream через callbacks

from itdpy import ITDClient
from itdpy.models import Notification, NotificationType

client = ITDClient(refresh_token="token")
stream = client.notifications.stream()


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


stream.run()
