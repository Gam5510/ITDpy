# 30_update_privacy.py
# Обновить privacy settings

from itdpy import ITDClient, AccessType

client = ITDClient(refresh_token="токен")

privacy = client.users.update_privacy(
    is_private=False,
    wall_access=AccessType.EVERYONE,
    likes_visibility=AccessType.EVERYONE,
    show_last_seen=True,
)

print(privacy)

client.close()
