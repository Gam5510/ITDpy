from uuid import UUID

from ..api.base import BaseAPI
from ..exceptions import APIError, NotFoundError, ValidationError
from ..models import NotificationsList
from ..streaming import NotificationStream


class NotificationsAPI(BaseAPI):
    @staticmethod
    def _validate_notification_id(notification_id: str) -> None:
        try:
            UUID(notification_id)
        except ValueError as exc:
            raise ValidationError(f"Invalid notification id: {notification_id}") from exc

    def list(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
    ) -> NotificationsList:
        params = {"limit": limit, "offset": offset}
        response = self._get("notifications", params=params)
        return NotificationsList.from_data(response.json())

    def list_all(self, *, limit: "int | None" = None) -> NotificationsList:
        items = []
        offset = 0
        total = None

        if limit is not None and limit <= 0:
            return NotificationsList([], total=0)

        while True:
            batch_limit = 50 if limit is None else min(50, limit - len(items))
            if batch_limit <= 0:
                break

            page = self.list(limit=batch_limit, offset=offset)
            items.extend(page.to_list())
            total = page.total

            if total is not None and len(items) >= total:
                break
            if len(page) < batch_limit:
                break
            if limit is not None and len(items) >= limit:
                break

            offset += batch_limit

        if limit is not None:
            items = items[:limit]

        return NotificationsList(items, total=total)

    def get_unread_count(self) -> int:
        response = self._get("notifications/count")
        data = response.json()
        if isinstance(data, dict):
            return data.get("count", data.get("unread", data.get("total", 0)))
        if isinstance(data, int):
            return data
        return 0

    def mark_read(self, notification_id: str) -> None:
        self._validate_notification_id(notification_id)
        try:
            self._post(f"notifications/{notification_id}/read")
        except APIError as exc:
            if exc.status_code == 500:
                raise NotFoundError(f"Notification not found: {notification_id}") from exc
            raise

    def mark_all_read(self) -> None:
        self._post("notifications/read-all")

    def stream(self, *, timeout: int = 60, max_backoff: int = 10) -> NotificationStream:
        return NotificationStream(
            self._request,
            self._token,
            timeout=timeout,
            max_backoff=max_backoff,
            on_token_refresh=self._request.get_token_refresh_callback(),
        )
