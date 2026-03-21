# 37_keep_online.py
# Поддерживать онлайн-статус

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")


def on_event(event_type, data):
    print(event_type, data)


thread = client.keep_online(on_event=on_event, background=True)

input("Press Enter to stop...\n")
client.close()
