from ..models.notifications import Notifications


def get_notifications(client, offset: int = 0, limit: int = 20):
    r = client.get(
        f"/api/notifications/?offset={offset}&limit={limit}"
    )
    r.raise_for_status()

    return Notifications(r.json())


def mark_notification_read(client, notification_id: str) -> bool:
    r = client.post(
        f"/api/notifications/{notification_id}/read"
    )
    r.raise_for_status()

    data = r.json()
    return data.get("success", False)

def mark_all_notification_read(client, notification_ids: list[str]) -> int:

    if not notification_ids:
        return 0
    
    if notification_ids is None:
        notification_ids = []
    elif isinstance(notification_ids, str):
        notification_ids = [notification_ids]

    r = client.post(
        "/api/notifications/read-batch",
        json=notification_ids
    )
    r.raise_for_status()

    data = r.json()
    return data.get("count", 0)
