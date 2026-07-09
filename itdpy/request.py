import json
import time
from typing import Optional, Dict, Any, Callable
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import Config
from .exceptions import (
    APIError,
    AccountBannedError,
    AlreadyBlockedError,
    AlreadyDeletedError,
    AlreadyFollowingError,
    AlreadyReportedError,
    AlreadyRepostedError,
    AuthenticationError,
    BannedWordError,
    BlockedUserError,
    CantBlockYourselfError,
    CantFollowYourselfError,
    CantRepostYourselfError,
    EditExpiredError,
    ForbiddenError,
    InvalidFileTypeError,
    ModerationFailedError,
    NetworkError,
    NotBlockedError,
    NotFoundError,
    NotMultipleChoiceError,
    NotPinnedError,
    OptionsNotBelongError,
    ProfileRequiredError,
    RateLimitError,
    RequiresSubscriptionError,
    RequiresVerificationError,
    SessionExpiredError,
    SessionNotFoundError,
    SessionRevokedError,
    TargetUserBannedError,
    UploadError,
    UsernameTakenError,
    ValidationError,
)

_ERROR_CODE_MAP: dict[str, type] = {
    "SESSION_NOT_FOUND": SessionNotFoundError,
    "SESSION_EXPIRED": SessionExpiredError,
    "SESSION_REVOKED": SessionRevokedError,
    "ACCOUNT_BANNED": AccountBannedError,
    "BANNED_WORD": BannedWordError,
    "MODERATION_FAILED": ModerationFailedError,
    "USERNAME_TAKEN": UsernameTakenError,
    "ALREADY_FOLLOWING": AlreadyFollowingError,
    "ALREADY_REPOSTED": AlreadyRepostedError,
    "ALREADY_BLOCKED": AlreadyBlockedError,
    "ALREADY_REPORTED": AlreadyReportedError,
    "ALREADY_DELETED": AlreadyDeletedError,
    "NOT_BLOCKED": NotBlockedError,
    "BLOCKED_USER": BlockedUserError,
    "CANT_FOLLOW_YOURSELF": CantFollowYourselfError,
    "CANT_REPOST_YOURSELF": CantRepostYourselfError,
    "CANT_BLOCK_YOURSELF": CantBlockYourselfError,
    "TARGET_USER_BANNED": TargetUserBannedError,
    "EDIT_EXPIRED": EditExpiredError,
    "NOT_PINNED": NotPinnedError,
    "OPTIONS_NOT_BELONG": OptionsNotBelongError,
    "NOT_MULTIPLE_CHOICE": NotMultipleChoiceError,
    "INVALID_FILE_TYPE": InvalidFileTypeError,
    "UPLOAD_ERROR": UploadError,
    "REQUIRES_SUBSCRIPTION": RequiresSubscriptionError,
    "REQUIRES_VERIFICATION": RequiresVerificationError,
    "PROFILE_REQUIRED": ProfileRequiredError,
}


class RequestHandler:

    def __init__(
        self,
        config: Config,
        on_token_refresh: Optional[Callable[[], str]] = None,
    ):
        self.config = config
        self.session = self._create_session()
        self._closed = False
        self._on_token_refresh = on_token_refresh
        self._token_refresh_in_progress = False
    
    def _create_session(self) -> requests.Session:
        session = requests.Session()
        
        retry_strategy = Retry(
            total=self.config.max_retries,
            backoff_factor=self.config.backoff_factor,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
            raise_on_status=False,
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        session.headers.update(self._build_default_headers())
        
        return session

    def _build_default_headers(self) -> dict[str, str]:
        headers = {
            "User-Agent": self.config.get_user_agent(),
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Origin": self.config.base_url,
            "Referer": f"{self.config.base_url}/",
        }
        if self.config.device_id:
            headers["x-device-id"] = self.config.device_id
        return headers
    
    def request(
        self,
        method: str,
        endpoint: str,
        *,
        access_token: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
        use_auth: bool = True,
    ) -> requests.Response:
        if self._closed:
            raise RuntimeError("Request handler is closed")
        
        url = self._build_url(endpoint)
        
        headers = {}
        if use_auth and access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        
        if timeout is None:
            timeout = self.config.upload_timeout if files else self.config.timeout
        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                params=params,
                json=json,
                files=files,
                headers=headers,
                timeout=timeout,
            )
            
            if response.status_code == 401 and use_auth and access_token and self._on_token_refresh and not self._token_refresh_in_progress:
                self._token_refresh_in_progress = True
                try:
                    new_token = self._on_token_refresh()
                    
                    headers["Authorization"] = f"Bearer {new_token}"
                    response = self.session.request(
                        method=method.upper(),
                        url=url,
                        params=params,
                        json=json,
                        files=files,
                        headers=headers,
                        timeout=timeout,
                    )
                finally:
                    self._token_refresh_in_progress = False
            
            self._handle_response(response)
            return response
            
        except requests.RequestException as e:
            raise NetworkError(f"Network error: {e}")
    
    def _build_url(self, endpoint: str) -> str:
        endpoint = endpoint.lstrip("/")
        return f"{self.config.base_url}/api/{endpoint}"

    def _handle_response(self, response: requests.Response) -> None:

        if response.ok:
            return

        error_info: dict | str | None = None
        error_code: str | None = None
        try:
            data = response.json()
            error_info = data.get('error', {})

            if isinstance(error_info, dict):
                error_code = error_info.get('code')
                error_message = (
                    error_info.get('message')
                    or data.get('message')
                    or data.get('detail')
                    or json.dumps(data, ensure_ascii=False)
                )
            else:
                error_code = None
                error_message = str(error_info) if error_info else json.dumps(data, ensure_ascii=False)
        except Exception:
            error_code = None
            error_message = response.text or f"HTTP {response.status_code}"

        if error_code and error_code in _ERROR_CODE_MAP:
            raise _ERROR_CODE_MAP[error_code](error_message)

        if response.status_code == 401:
            raise AuthenticationError(error_message)
        elif response.status_code == 403:
            raise ForbiddenError(error_message)
        elif response.status_code == 404:
            raise NotFoundError(error_message)
        elif response.status_code == 422:
            raise ValidationError(error_message)
        elif response.status_code == 429:
            retry_after = self._get_retry_after(response, error_info if isinstance(error_info, dict) else {})
            raise RateLimitError(error_message, retry_after=retry_after)
        else:
            raise APIError(error_message, status_code=response.status_code)
    
    def _get_retry_after(self, response: requests.Response, error_info: dict) -> int:

        retry_after = response.headers.get('Retry-After')
        if retry_after:
            try:
                return int(retry_after)
            except:
                pass
        
        if error_info:
            retry_after = error_info.get('retryAfter')
            if retry_after:
                return int(retry_after)
        
        return 60
    
    def close(self) -> None:
        if not self._closed:
            self.session.close()
            self._closed = True

    def get_token_refresh_callback(self) -> Optional[Callable[[], str]]:
        return self._on_token_refresh
