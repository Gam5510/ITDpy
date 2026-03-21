from dataclasses import dataclass


@dataclass
class Config:
    
    base_url: str = "https://xn--d1ah4a.com"
    timeout: int = 20
    upload_timeout: int = 120
    max_retries: int = 3
    backoff_factor: float = 1.5
    sdk_version: str = "1.0.1"
