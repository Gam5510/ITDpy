# 32_notifications_list.py
# Получить уведомления

from itdpy import ITDClient

client = ITDClient(refresh_token="token")

notifications = client.notifications.list(limit=20)

print(len(notifications))
for notification in notifications:
    print(notification.id, notification.type, notification.actor.username)

client.close()
