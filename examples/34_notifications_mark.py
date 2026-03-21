# 34_notifications_mark.py
# Прочитать уведомления

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

client.notifications.mark_read("ID")
client.notifications.mark_all_read()

client.close()
