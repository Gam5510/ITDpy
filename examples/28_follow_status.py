# 28_follow_status.py
# Проверка follow-status списком user ids

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

statuses = client.users.follow_status([
    "091cd083-d146-434e-aa4a-39bb48fdaf81",
    "0aaf3e2c-f878-426d-abc1-21c562919995",
])

for item in statuses:
    print(item.id, item.is_following)
    print(item.to_dict())

client.close()
