# 33_notifications_all.py
# Получить все уведомления

from itdpy import ITDClient

client = ITDClient(refresh_token="token")

notifications_100 = client.notifications.list_all(limit=100)

print(len(notifications_100))
print(notifications_100.first())

notifications_all = client.notifications.list_all()

print(len(notifications_all))
print(notifications_all.first())

client.close()
