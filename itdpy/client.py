import base64
import json
import logging
import random
import threading
import time
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
from .profiles import Profile, ProfileStore
from .request import RequestHandler

logger = logging.getLogger("itdpy.client")


def _decode_jwt_exp(token: str) -> Optional[float]:
    try:
        payload_b64 = token.split(".")[1]
        payload_b64 += "=" * (-len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        return payload.get("exp")
    except Exception:
        return None


class ITDClient:
    def __init__(
        self,
        refresh_token: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        profile: Optional[str] = None,
        profiles_path: Optional[str] = None,
        device_id: Optional[str] = None,
        config: Optional[Config] = None,
        on_refresh_token_update: Optional[Callable[[str], None]] = None,
        browser_path: Optional[str] = None,
        auto_refresh_interval: Optional[tuple] = (13 * 60, 14 * 60),
        turnstile_timeout: int = 60,
        login_attempts: int = 2,
    ):
        self._profile_name = profile
        self._profile_store = ProfileStore(profiles_path) if profile else None

        self._param_refresh_token = refresh_token
        self._param_email = email
        self._param_device_id = device_id

        if self._profile_store:
            saved = self._profile_store.load(profile)
            if saved and saved.refresh_token:
                refresh_token = saved.refresh_token
                email = email or saved.email
                device_id = device_id or saved.device_id

        if not refresh_token and not (email and password):
            raise AuthenticationError(
                "Необходимо указать либо refresh_token, либо email и password, "
                "либо profile с уже сохранёнными данными"
            )

        self.config = config or Config()
        if device_id:
            self.config.device_id = device_id
        self._email = email or self._param_email
        self._password = password
        self._browser_path = browser_path
        self._turnstile_timeout = turnstile_timeout
        self._login_attempts = login_attempts
        self._on_refresh_token_update = on_refresh_token_update
        self._access_token: Optional[str] = None
        self._access_expires_at: Optional[float] = None
        self._user_id: Optional[str] = None

        if not refresh_token:
            logger.info("refresh_token не передан, выполняем вход по email/password")
            refresh_token = self._login()

        self._refresh_token = refresh_token

        self._request_handler = RequestHandler(
            self.config,
            on_token_refresh=self._refresh_access_token,
        )

        self._authenticate_with_fallback(self._authenticate)

        if self._profile_store:
            self._profile_store.save(Profile(
                name=self._profile_name,
                refresh_token=self._refresh_token,
                access_token=self._access_token,
                access_expires_at=self._access_expires_at,
                email=self._email,
                user_id=self._user_id,
                device_id=self.config.device_id,
            ))

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
        self._access_expires_at = _decode_jwt_exp(self._access_token) if self._access_token else None
        self._capture_rotated_refresh_token(response)

        if not self._access_token:
            raise AuthenticationError("Failed to get access token")

        me_response = self._request_handler.request(
            method="GET",
            endpoint="users/me",
            access_token=self._access_token,
        )
        self._user_id = me_response.json().get("id")
        self._update_user_agent()

    def _refresh_only(self) -> None:
        response = self._request_handler.request(
            method="POST",
            endpoint="v1/auth/refresh",
            use_auth=False,
        )
        data = response.json()
        new_access_token = data.get("accessToken")
        self._capture_rotated_refresh_token(response)

        if not new_access_token:
            raise AuthenticationError("Failed to refresh access token")

        self._access_token = new_access_token
        self._access_expires_at = _decode_jwt_exp(new_access_token)

    def _refresh_access_token(self) -> str:
        self._authenticate_with_fallback(self._refresh_only)
        self._persist_profile()
        return self._access_token

    def _resolve_candidate_tokens(self) -> list:
        candidates = []
        if self._profile_store:
            saved = self._profile_store.load(self._profile_name)
            if saved and saved.refresh_token:
                candidates.append(saved.refresh_token)
        if self._param_refresh_token:
            candidates.append(self._param_refresh_token)
        if self._refresh_token:
            candidates.append(self._refresh_token)

        seen = set()
        unique = []
        for token in candidates:
            if token not in seen:
                seen.add(token)
                unique.append(token)
        return unique

    def _authenticate_with_fallback(self, action: Callable[[], None]) -> None:
        last_error = None
        for token in self._resolve_candidate_tokens():
            self._refresh_token = token
            self._setup_session()
            try:
                action()
                return
            except AuthenticationError as e:
                last_error = e
                logger.warning(
                    "Аутентификация с текущим refresh_token не удалась (%s), "
                    "пробуем следующий доступный вариант", e,
                )

        if self._email and self._password:
            logger.warning(
                "Ни один сохранённый refresh_token не сработал (%s), "
                "перелогиниваемся по email/password", last_error,
            )
            self._refresh_token = self._login()
            self._setup_session()
            action()
            return

        if last_error:
            raise last_error
        raise AuthenticationError("Failed to authenticate: no valid refresh_token available")

    def _login(self) -> str:
        return login_with_password(
            self._email,
            self._password,
            browser_path=self._browser_path,
            max_wait_time=self._turnstile_timeout,
            attempts=self._login_attempts,
        )

    def _capture_rotated_refresh_token(self, response=None) -> None:
        jar = self._request_handler.session.cookies

        new_refresh_token = None
        if response is not None:
            for cookie in response.cookies:
                if cookie.name == "refresh_token" and cookie.value:
                    new_refresh_token = cookie.value

        if not new_refresh_token:
            candidates = [c.value for c in jar if c.name == "refresh_token" and c.value]
            new_refresh_token = candidates[-1] if candidates else None

        for cookie in list(jar):
            if cookie.name == "refresh_token":
                jar.clear(cookie.domain, cookie.path, cookie.name)

        effective_token = new_refresh_token or self._refresh_token
        jar.set("refresh_token", effective_token, domain="xn--d1ah4a.com", path="/")

        if not new_refresh_token or new_refresh_token == self._refresh_token:
            return

        self._refresh_token = new_refresh_token
        if self._on_refresh_token_update:
            self._on_refresh_token_update(new_refresh_token)
        self._persist_profile()

    def _persist_profile(self) -> None:
        if not self._profile_store:
            return
        self._profile_store.touch(
            self._profile_name,
            refresh_token=self._refresh_token,
            access_token=self._access_token,
            access_expires_at=self._access_expires_at,
            email=self._email,
            user_id=self._user_id,
            device_id=self.config.device_id,
        )

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

    @property
    def access_expires_at(self) -> Optional[float]:
        return self._access_expires_at


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

    def start_auto_refresh(
        self, interval: Optional[tuple] = (13 * 60, 14 * 60),
    ) -> threading.Thread:
        self.stop_auto_refresh()
        self._auto_refresh_stop.clear()

        def _next_delay() -> float:
            if isinstance(interval, (tuple, list)):
                return random.uniform(interval[0], interval[1])
            return interval

        def _run():
            while not self._auto_refresh_stop.wait(_next_delay()):
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