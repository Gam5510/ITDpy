from .user_lite import UserLite


class Users:
    def __init__(self, response: dict):
        data = response.get("data", {})

        self._items = [UserLite(u) for u in data.get("users", [])]

        pagination = data.get("pagination", {})
        self.page = pagination.get("page")
        self.limit = pagination.get("limit")
        self.total = pagination.get("total")
        self.has_more = pagination.get("hasMore")

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __repr__(self):
        return f"<Users count={len(self)}>"
