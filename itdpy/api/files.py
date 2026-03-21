from ..api.base import BaseAPI
from ..models import File


class FilesAPI(BaseAPI):
    
    def upload(self, file_path: str) -> File:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = self._post("files/upload", files=files)
        return File.model_validate(response.json())
    
    def get(self, file_id: str) -> File:
        response = self._get(f"files/{file_id}")
        return File.model_validate(response.json())
    
    def delete(self, file_id: str) -> None:
      self._delete(f"files/{file_id}")
