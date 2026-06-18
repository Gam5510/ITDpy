"""Example: stream real-time notifications."""
from itdpy import ITDClient

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    print("Listening for notifications (Ctrl+C to stop)...")
    for event in client.notifications.stream():
        if event.event != "connected":
            print(f"Event: {event.event} | Data: {event.data}")
