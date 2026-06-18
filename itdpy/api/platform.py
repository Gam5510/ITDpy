from ..api.base import BaseAPI
from ..models import App, Changelog


class PlatformAPI(BaseAPI):
    def version(self) -> dict:
        response = self._get("platform/version")
        data = response.json()
        if isinstance(data, dict):
            result = {}
            for name, info in data.items():
                if isinstance(info, dict):
                    info["name"] = name
                    try:
                        result[name] = App.model_validate(info)
                    except Exception:
                        result[name] = info
            return result
        return data

    def get_changelog(self) -> Changelog:
        response = self._get("platform/changelog")
        return Changelog.from_data(response.json())
