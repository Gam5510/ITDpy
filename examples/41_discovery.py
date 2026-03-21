# 41_discovery.py
# Discovery API

from itdpy import ITDClient

client = ITDClient(refresh_token="token")

top_clans = client.discovery.get_top_clans()
who_to_follow = client.discovery.who_to_follow()
portal = client.discovery.portal()
if portal.active:
    print("portal:", portal.to_dict())
    print("portal title:", portal.title)
    print("url:", portal.url)
print("top clans:")
for clan in top_clans:
    print(clan.avatar, clan.get("member_count"))

print("who to follow:")
for user in who_to_follow:
    print(user.username, user.display_name, user.get("avatar"))

client.close()
