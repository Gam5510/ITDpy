import threading
import warnings
from typing import Optional

from .api import (
    CommentsAPI,
    DiscoveryAPI,
    FilesAPI,
    HashtagsAPI,
    NotificationsAPI,
    PinsAPI,
    PlatformAPI,
    PostsAPI,
    SearchAPI,
    SessionsAPI,
    UsersAPI,
    VerificationAPI,
)
from .config import Config
from .exceptions import AuthenticationError, ITDAttributeError
from .request import RequestHandler

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

        self._request_handler = RequestHandler(
            self.config,
            on_token_refresh=self._refresh_access_token,
        )

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
        self._sessions: Optional[SessionsAPI] = None
        self._hashtags: Optional[HashtagsAPI] = None
        self._verification: Optional[VerificationAPI] = None
        self._platform: Optional[PlatformAPI] = None
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

    def _refresh_access_token(self) -> str:
        response = self._request_handler.request(
            method="POST",
            endpoint="v1/auth/refresh",
            use_auth=False,
        )
        data = response.json()
        new_access_token = data.get("accessToken")

        if not new_access_token:
            raise AuthenticationError("Failed to refresh access token")

        self._access_token = new_access_token
        return new_access_token

    def _update_user_agent(self) -> None:
        ua = self.config.get_user_agent(user_id=self._user_id)
        self._request_handler.session.headers["User-Agent"] = ua


    @property
    def access_token(self) -> Optional[str]:
        return self._access_token

    @property
    def user_id(self) -> Optional[str]:
        return self._user_id


    def _api(self, attr: str, cls):
        self._check_closed()
        val = getattr(self, attr)
        if val is None:
            val = cls(self._request_handler, self._access_token)
            setattr(self, attr, val)
        return val

    @property
    def posts(self) -> PostsAPI:
        return self._api("_posts", PostsAPI)

    @property
    def users(self) -> UsersAPI:
        return self._api("_users", UsersAPI)

    @property
    def comments(self) -> CommentsAPI:
        return self._api("_comments", CommentsAPI)

    @property
    def notifications(self) -> NotificationsAPI:
        return self._api("_notifications", NotificationsAPI)

    @property
    def files(self) -> FilesAPI:
        return self._api("_files", FilesAPI)

    @property
    def search(self) -> SearchAPI:
        return self._api("_search", SearchAPI)

    @property
    def pins(self) -> PinsAPI:
        return self._api("_pins", PinsAPI)

    @property
    def discovery(self) -> DiscoveryAPI:
        return self._api("_discovery", DiscoveryAPI)
    
    @property
    def sessions(self) -> SessionsAPI:
        return self._api("_sessions", SessionsAPI)

    @property
    def hashtags(self) -> HashtagsAPI:
        return self._api("_hashtags", HashtagsAPI)

    @property
    def verification(self) -> VerificationAPI:
        return self._api("_verification", VerificationAPI)

    @property
    def platform(self) -> PlatformAPI:
        return self._api("_platform", PlatformAPI)

    def close(self) -> None:
        if not self._closed:
            self._request_handler.close()
            self._closed = True

    def _check_closed(self) -> None:
        if self._closed:
            raise RuntimeError("Client is closed")

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