from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Callable, Iterator, Optional

import requests

from .exceptions import NetworkError
from .models import ConnectedEventData, Notification
from .enums import NotificationType
from .request import RequestHandler


@dataclass(slots=True)
class StreamEvent:
    event: str
    data: dict[str, object] | ConnectedEventData | Notification | None
    raw_data: str | None = None
    event_id: str | None = None


@dataclass(slots=True)
class _HandlerSubscription:
    callback: Callable[[StreamEvent], None]
    notification_type: NotificationType | None = None


class NotificationStream:
    def __init__(
        self,
        request_handler: RequestHandler,
        access_token: str,
        *,
        endpoint: str = "notifications/stream",
        timeout: int = 60,
        max_backoff: int = 10,
        on_token_refresh: Optional[Callable[[], str]] = None,
    ):
        self._request = request_handler
        self._access_token = access_token
        self._endpoint = endpoint
        self._timeout = timeout
        self._max_backoff = max_backoff
        self._stopped = False
        self._last_event_id: str | None = None
        self._handlers: dict[str, list[_HandlerSubscription]] = {}
        self._active_response: requests.Response | None = None
        self._on_token_refresh = on_token_refresh

    def on(
        self,
        event_name: str,
        *,
        type: NotificationType | None = None,
    ) -> Callable[[Callable[[StreamEvent], None]], Callable[[StreamEvent], None]]:
        def decorator(handler: Callable[[StreamEvent], None]) -> Callable[[StreamEvent], None]:
            subscription = _HandlerSubscription(
                callback=handler,
                notification_type=type,
            )
            self._handlers.setdefault(event_name, []).append(subscription)
            return handler

        return decorator

    def stop(self) -> None:
        self._stopped = True
        self._close_active_response()

    def run(self) -> None:
        try:
            for _ in self:
                pass
        except KeyboardInterrupt:
            self.stop()

    def __iter__(self) -> Iterator[StreamEvent]:
        backoff = 1

        while not self._stopped:
            response: requests.Response | None = None
            try:
                response = self._connect()
                self._active_response = response
                backoff = 1

                client = self._create_sse_client(response)
                for sse_event in client.events():
                    if self._stopped:
                        response.close()
                        return

                    parsed_event = self._parse_event(sse_event)
                    if parsed_event is None:
                        continue

                    self._dispatch(parsed_event)
                    yield parsed_event
            except KeyboardInterrupt:
                self.stop()
                return
            except requests.RequestException as exc:
                error_event = StreamEvent(event="error", data={"message": str(exc)})
                self._dispatch(error_event)
                yield error_event
            except NetworkError as exc:
                error_event = StreamEvent(event="error", data={"message": str(exc)})
                self._dispatch(error_event)
                yield error_event
            finally:
                if response is not None:
                    response.close()
                if self._active_response is response:
                    self._active_response = None

            if self._stopped:
                break

            reconnect_event = StreamEvent(event="reconnecting", data={"delay": backoff})
            self._dispatch(reconnect_event)

            if self._on_token_refresh:
                try:
                    self._access_token = self._on_token_refresh()
                except Exception as exc:
                    refresh_error_event = StreamEvent(
                        event="error", 
                        data={"message": f"Token refresh failed: {str(exc)}"}
                    )
                    self._dispatch(refresh_error_event)
                    yield refresh_error_event
            
            try:
                time.sleep(backoff)
            except KeyboardInterrupt:
                self.stop()
                break
            backoff = min(self._next_backoff(backoff), self._max_backoff)

    def _connect(self) -> requests.Response:
        url = self._request._build_url(self._endpoint)
        headers = {
            "Accept": "text/event-stream",
            "Cache-Control": "no-cache",
            "Authorization": f"Bearer {self._access_token}",
        }
        if self._last_event_id:
            headers["Last-Event-ID"] = self._last_event_id

        response = self._request.session.get(
            url,
            headers=headers,
            stream=True,
            timeout=self._timeout,
        )
        self._request._handle_response(response)
        return response

    @staticmethod
    def _create_sse_client(response: requests.Response):
        try:
            from sseclient import SSEClient
        except ImportError as exc:
            raise RuntimeError(
                "SSE support requires 'sseclient-py'. Install it with: pip install sseclient-py"
            ) from exc

        return SSEClient(response)

    def _parse_event(self, sse_event) -> StreamEvent | None:
        event_name = sse_event.event or "message"
        raw_data = sse_event.data

        if event_name == "ping" or raw_data in (None, "", "ping"):
            return None

        if sse_event.id:
            self._last_event_id = sse_event.id

        payload = self._parse_data(event_name, raw_data)
        return StreamEvent(
            event=event_name,
            data=payload,
            raw_data=raw_data,
            event_id=sse_event.id,
        )

    def _parse_data(self, event_name: str, raw_data: str) -> dict[str, object] | ConnectedEventData | Notification | None:
        try:
            payload = json.loads(raw_data)
        except json.JSONDecodeError:
            return {"raw": raw_data}

        if event_name == "connected" and isinstance(payload, dict):
            return ConnectedEventData.model_validate(payload)

        if event_name == "notification" and isinstance(payload, dict):
            return Notification.model_validate(payload)

        return payload if isinstance(payload, dict) else {"value": payload}

    def _dispatch(self, event: StreamEvent) -> None:
        for subscription in self._handlers.get(event.event, []):
            if (
                subscription.notification_type is not None
                and isinstance(event.data, Notification)
                and event.data.type != subscription.notification_type
            ):
                continue
            if subscription.notification_type is not None and not isinstance(event.data, Notification):
                continue
            subscription.callback(event)

    @staticmethod
    def _next_backoff(current: int) -> int:
        if current < 2:
            return 2
        if current < 5:
            return 5
        return current * 2

    def _close_active_response(self) -> None:
        if self._active_response is None:
            return

        try:
            self._active_response.close()
        finally:
            self._active_response = None
