from ..api.base import BaseAPI
from ..models import VerificationRequest, VerificationStatus


class VerificationAPI(BaseAPI):

    def submit(self, video_url: str) -> VerificationRequest:
        response = self._post("verification/submit", json={"videoUrl": video_url})
        data = response.json()
        if isinstance(data, dict) and "request" in data:
            return VerificationRequest.model_validate(data["request"])
        if isinstance(data, dict) and "data" in data:
            return VerificationRequest.model_validate(data["data"])
        return VerificationRequest.model_validate(data)

    def get_status(self) -> VerificationStatus:
        response = self._get("verification/status")
        data = response.json()
        if isinstance(data, dict) and "data" in data:
            data = data["data"]
        return VerificationStatus.model_validate(data)
