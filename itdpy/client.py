from typing import Optional
import threading
import warnings

from .api import CommentsAPI, DiscoveryAPI, FilesAPI, NotificationsAPI, PinsAPI, PostsAPI, SearchAPI, UsersAPI
from .config import Config
from .exceptions import AuthenticationError, ITDAttributeError
from .request import RequestHandler
from .utils.suggestions import get_suggestion


class ITDClient:
    def __init__(
        self,
        refresh_token: str,
        config: Optional[Config] = None,
    ):
        self.config = config or Config()
        self._refresh_token = refresh_token
        self._access_token: Optional[str] = None
        self._user_id: Optional[str] = None

        self._request_handler = RequestHandler(self.config)

        self._setup_session()
        self._authenticate()

        self._posts: Optional[PostsAPI] = None
        self._users: Optional[UsersAPI] = None
        self._comments: Optional[CommentsAPI] = None
        self._notifications: Optional[NotificationsAPI] = None
        self._files: Optional[FilesAPI] = None
        self._search: Optional[SearchAPI] = None
        self._pins: Optional[PinsAPI] = None
        self._discovery: Optional[DiscoveryAPI] = None
        self._closed = False

    def _setup_session(self) -> None:
        self._request_handler.session.cookies.set(
            name="refresh_token",
            value=self._refresh_token,
            domain="xn--d1ah4a.com",
            path="/",
        )

    def _authenticate(self) -> None:
        response = self._request_handler.request(
            method="POST",
            endpoint="v1/auth/refresh",
            use_auth=False,
        )

        data = response.json()
        self._access_token = data.get("accessToken")

        if not self._access_token:
            raise AuthenticationError("Failed to get access token")

        me_response = self._request_handler.request(
            method="GET",
            endpoint="users/me",
            access_token=self._access_token,
        )

        self._user_id = me_response.json().get("id")
        self._update_user_agent()

    def _update_user_agent(self) -> None:
        if self.config.custom_user_agent:
            self._request_handler.session.headers["User-Agent"] = self.config.custom_user_agent
            return

        if not self.config.use_user_data_in_user_agent:
            self._request_handler.session.headers["User-Agent"] = self.config.initial_user_agent
            return

        parts = [f"platform=python"]
        if self._user_id:
            parts.insert(0, f"userid={self._user_id}")
        else:
            parts.insert(0, "initial")
        if self.config.service:
            parts.append(f"service={self.config.service}")

        user_agent = self.config.user_agent_template.format(
            sdk_version=self.config.sdk_version,
            parts="; ".join(parts),
            user_id=self._user_id or "",
            service=self.config.service or "",
        )
        self._request_handler.session.headers["User-Agent"] = user_agent

    @property
    def access_token(self) -> Optional[str]:
        return self._access_token

    @property
    def user_id(self) -> Optional[str]:
        return self._user_id

    @property
    def posts(self) -> PostsAPI:
        self._check_closed()
        if self._posts is None:
            self._posts = PostsAPI(self._request_handler, self._access_token)
        return self._posts

    @property
    def users(self) -> UsersAPI:
        self._check_closed()
        if self._users is None:
            self._users = UsersAPI(self._request_handler, self._access_token)
        return self._users

    @property
    def comments(self) -> CommentsAPI:
        self._check_closed()
        if self._comments is None:
            self._comments = CommentsAPI(self._request_handler, self._access_token)
        return self._comments

    @property
    def notifications(self) -> NotificationsAPI:
        self._check_closed()
        if self._notifications is None:
            self._notifications = NotificationsAPI(self._request_handler, self._access_token)
        return self._notifications

    @property
    def files(self) -> FilesAPI:
        self._check_closed()
        if self._files is None:
            self._files = FilesAPI(self._request_handler, self._access_token)
        return self._files

    @property
    def search(self) -> SearchAPI:
        self._check_closed()
        if self._search is None:
            self._search = SearchAPI(self._request_handler, self._access_token)
        return self._search

    @property
    def pins(self) -> PinsAPI:
        self._check_closed()
        if self._pins is None:
            self._pins = PinsAPI(self._request_handler, self._access_token)
        return self._pins

    @property
    def discovery(self) -> DiscoveryAPI:
        self._check_closed()
        if self._discovery is None:
            self._discovery = DiscoveryAPI(self._request_handler, self._access_token)
        return self._discovery

    def close(self):
        if not self._closed:
            self._request_handler.close()
            self._closed = True

    def _check_closed(self):
        if self._closed:
            raise RuntimeError("Client is closed")

    @staticmethod
    def _warn_deprecated(old_name: str, new_call: str) -> None:
        warnings.warn(
            f"'{old_name}' устарел. Используй {new_call}",
            DeprecationWarning,
            stacklevel=2,
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def keep_online(self, on_event=None, background: bool = True):
        def _run():
            stream = self.notifications.stream()
            for event in stream:
                if on_event and event.event != "connected":
                    on_event(event.event, event.data)

        if background:
            thread = threading.Thread(target=_run, daemon=True)
            thread.start()
            return thread

        _run()
        return None

    def __getattr__(self, name: str):
        suggestion = get_suggestion(name)

        red = "\033[91m"
        reset = "\033[0m"

        message = f"""
{red}
⚠️  WARNING - Breaking Changes in 1.x

Метод '{name}' не существует или был удалён.

👉 Используйте:
{suggestion}

📖 Migration guide:
https://gam5510.github.io/ITDpy/MIGRATION/
{reset}
"""
        raise ITDAttributeError(message)
