# 31_update_notification_settings.py
# Обновить notification settings

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

settings = client.users.update_notification_settings(
    enabled=True,
    comments=True,
    follows=True,
    likes=True,
    mentions=True,
    sound=True,
    wall_posts=True,
)

print(settings)

client.close()
