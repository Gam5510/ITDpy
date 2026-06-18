"""Example: mark all notifications as read."""
from itdpy import ITDClient

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    count = client.notifications.get_unread_count()
    print(f"Unread before: {count}")
    client.notifications.mark_all_read()
    print("Marked all as read.")
