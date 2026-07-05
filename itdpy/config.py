from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Config:
    base_url: str = "https://xn--d1ah4a.com"
    timeout: int = 20
    upload_timeout: int = 120
    max_retries: int = 3
    backoff_factor: float = 1.5

    sdk_version: str = "1.2.0"
    service: Optional[str] = None

    use_user_data_in_user_agent: bool = False
    custom_user_agent: Optional[str] = None

    def get_user_agent(self, user_id: Optional[str] = None) -> str:
        if self.custom_user_agent:
            return self.custom_user_agent

        parts = []

        if self.use_user_data_in_user_agent:
            if user_id:
                parts.append(f"userid={user_id}")
            else:
                parts.append("initial")

        parts.append("platform=python")

        if self.service:
            parts.append(f"service={self.service}")

        parts_str = "; ".join(parts)
        return f"ITDpy/{self.sdk_version} ({parts_str})"
