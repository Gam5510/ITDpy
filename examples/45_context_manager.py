# 45_context_manager.py
# Использование через with

from itdpy import ITDClient

with ITDClient(refresh_token="токен") as client:
    me = client.users.me()
    print(me.username)
