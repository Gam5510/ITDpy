from .notification import Notification


class Notifications:
    def __init__(self, response: dict):
        items = response.get("notifications", [])

        self._items = [Notification(n) for n in items]
        self.has_more = response.get("hasMore", False)

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __repr__(self):
        return f"<Notifications count={len(self)}>"
