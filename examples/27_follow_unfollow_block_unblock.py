# 27_follow_unfollow_block_unblock.py
# Follow / unfollow / block / unblock

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

client.users.unfollow("fufelshmerch")
client.users.follow("fufelshmerch")


client.users.block("vilant")
client.users.unblock("vilant")

client.close()
