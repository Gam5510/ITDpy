from dataclasses import dataclass


@dataclass
class Config:
    base_url: str = "https://xn--d1ah4a.com"
    timeout: int = 20
    upload_timeout: int = 120
    max_retries: int = 3
    backoff_factor: float = 1.5
    sdk_version: str = "1.0.2"
    service: str | None = None
    initial_user_agent: str = (
        "Mozilla/5.0 (Linux; Android 11; SM-G991B)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/120.0.6099.144 Mobile Safari/537.36"
    )
    custom_user_agent: str | None = None
    user_agent_template: str = "itdpy/{sdk_version} ({parts})"
    use_user_data_in_user_agent: bool = False
