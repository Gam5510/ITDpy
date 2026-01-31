from .post import Post
import json

class Posts:
    def __init__(self, response: dict):
        data = response.get("data")
        self._data = data 

        if isinstance(data, list):
            items = data
            pagination = {}

        elif isinstance(data, dict):
            items = data.get("posts", [])
            pagination = data.get("pagination", {})

        else:
            items = []
            pagination = {}

        self._items = [Post(item) for item in items]

        self.limit = pagination.get("limit")
        self.next_cursor = pagination.get("nextCursor")
        self.has_more = pagination.get("hasMore")

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __repr__(self):
        return f"<Posts count={len(self)}>"
    
    def __str__(self):
        return json.dumps(self._data, ensure_ascii=False)