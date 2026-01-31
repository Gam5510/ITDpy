import json

class Attachment:
    def __init__(self, data: dict):
        self._data = data
        self.id = data.get("id")
        self.url = data.get("url")
        self.filename = data.get("filename")
        self.mimeType = data.get("mimeType")
        self.size = data.get("size")
    def __str__(self):
        return json.dumps(self._data, ensure_ascii=False)