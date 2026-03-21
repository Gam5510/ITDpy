import json
import time
from typing import Optional, Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import Config
from .exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    NetworkError,
)


class RequestHandler:

    def __init__(self, config: Config):
        self.config = config
        self.session = self._create_session()
        self._closed = False
    
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
        
        return session
    
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
            
            self._handle_response(response)
            return response
            
        except requests.RequestException as e:
            raise NetworkError(f"Network error: {e}")
    
    def _build_url(self, endpoint: str) -> str:
        if not endpoint.startswith('/'):
            endpoint = f'/{endpoint}'
        return f"{self.config.base_url}/api{endpoint}"
    
    def _handle_response(self, response: requests.Response) -> None:

        if response.ok:
            return

        error_info: dict | str | None = None
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
        except:
            error_code = None
            error_message = response.text or f"HTTP {response.status_code}"
        
        if response.status_code == 401:
            raise AuthenticationError(error_message)
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
