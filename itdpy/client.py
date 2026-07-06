import logging
import threading
import warnings
from typing import Callable, Optional

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
from .auth import login_with_password
from .config import Config
from .exceptions import AuthenticationError
from .request import RequestHandler

logger = logging.getLogger("itdpy.client")


class ITDClient:
    def __init__(
        self,
        refresh_token: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        config: Optional[Config] = None,
        on_refresh_token_update: Optional[Callable[[str], None]] = None,
        browser_path: Optional[str] = None,
        auto_refresh_interval: Optional[int] = 270,
        turnstile_timeout: int = 60,
        login_attempts: int = 2,
    ):
        if not refresh_token and not (email and password):
            raise AuthenticationError(
                "Необходимо указать либо refresh_token, либо email и password"
            )

        self.config = config or Config()
        self._email = email
        self._password = password
        self._browser_path = browser_path
        self._turnstile_timeout = turnstile_timeout
        self._login_attempts = login_attempts
        self._on_refresh_token_update = on_refresh_token_update
        self._access_token: Optional[str] = None
        self._user_id: Optional[str] = None

        if not refresh_token:
            logger.info("refresh_token не передан, выполняем вход по email/password")
            refresh_token = self._login()

        self._refresh_token = refresh_token

        self._request_handler = RequestHandler(
            self.config,
            on_token_refresh=self._refresh_access_token,
        )

        self._setup_session()
        try:
            self._authenticate()
        except AuthenticationError as e:
            if not (self._email and self._password):
                raise
            logger.warning(
                "Аутентификация по сохранённому refresh_token не удалась (%s), "
                "перелогиниваемся по email/password", e,
            )
            self._refresh_token = self._login()
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

        self._auto_refresh_stop = threading.Event()
        self._auto_refresh_thread: Optional[threading.Thread] = None
        if auto_refresh_interval:
            self.start_auto_refresh(auto_refresh_interval)


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
        self._capture_rotated_refresh_token()

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
        try:
            response = self._request_handler.request(
                method="POST",
                endpoint="v1/auth/refresh",
                use_auth=False,
            )
            data = response.json()
            new_access_token = data.get("accessToken")
        except AuthenticationError as e:
            if not (self._email and self._password):
                raise
            logger.warning(
                "Не удалось обновить access_token (%s), перелогиниваемся по email/password", e,
            )
            self._refresh_token = self._login()
            self._setup_session()
            response = self._request_handler.request(
                method="POST",
                endpoint="v1/auth/refresh",
                use_auth=False,
            )
            data = response.json()
            new_access_token = data.get("accessToken")

        self._capture_rotated_refresh_token()

        if not new_access_token:
            raise AuthenticationError("Failed to refresh access token")

        self._access_token = new_access_token
        return new_access_token

    def _login(self) -> str:
        return login_with_password(
            self._email,
            self._password,
            browser_path=self._browser_path,
            max_wait_time=self._turnstile_timeout,
            attempts=self._login_attempts,
        )

    def _capture_rotated_refresh_token(self) -> None:
        new_refresh_token = self._request_handler.session.cookies.get(
            "refresh_token", domain="xn--d1ah4a.com",
        )
        if not new_refresh_token or new_refresh_token == self._refresh_token:
            return

        self._refresh_token = new_refresh_token
        if self._on_refresh_token_update:
            self._on_refresh_token_update(new_refresh_token)

    def _update_user_agent(self) -> None:
        ua = self.config.get_user_agent(user_id=self._user_id)
        self._request_handler.session.headers["User-Agent"] = ua


    @property
    def access_token(self) -> Optional[str]:
        return self._access_token

    @property
    def user_id(self) -> Optional[str]:
        return self._user_id

    @property
    def refresh_token(self) -> str:
        return self._refresh_token


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

    def start_auto_refresh(self, interval: int = 270) -> threading.Thread:
        self.stop_auto_refresh()
        self._auto_refresh_stop.clear()

        def _run():
            while not self._auto_refresh_stop.wait(interval):
                if self._closed:
                    return
                try:
                    self._refresh_access_token()
                    logger.debug("Access token обновлён по расписанию")
                except Exception:
                    logger.exception("Ошибка планового обновления access_token")

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        self._auto_refresh_thread = thread
        return thread

    def stop_auto_refresh(self) -> None:
        self._auto_refresh_stop.set()
        if self._auto_refresh_thread and self._auto_refresh_thread.is_alive():
            self._auto_refresh_thread.join(timeout=1)
        self._auto_refresh_thread = None

    def close(self) -> None:
        if not self._closed:
            self.stop_auto_refresh()
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