# 35_stream_for_loop.py
# SSE stream через for-loop

from itdpy import ITDClient
from itdpy.models import ConnectedEventData, Notification

client = ITDClient(refresh_token="token")

for event in client.notifications.stream():
    if event.event == "connected":
        data: ConnectedEventData = event.data
        print(data.user_id, data.timestamp)

    if event.event == "notification":
        notification: Notification = event.data
        print(notification.type, notification.actor.display_name, notification.preview)
        break

client.close()
