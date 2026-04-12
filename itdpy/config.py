from dataclasses import dataclass
from typing import Optional
import warnings


@dataclass
class Config:
    # Базовые настройки
    base_url: str = "https://xn--d1ah4a.com"
    timeout: int = 20
    upload_timeout: int = 120
    max_retries: int = 3
    backoff_factor: float = 1.5
    sdk_version: str = "1.0.5"
    service: str | None = None
    use_user_data_in_user_agent: bool = False

    def get_user_agent(self, user_id: Optional[str] = None) -> str:
        return self._build_safe_user_agent(user_id)

    def _build_safe_user_agent(self, user_id: Optional[str] = None) -> str:
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

        user_agent_template = "itdpy/{sdk_version} ({parts})"
        
        return user_agent_template.format(
            sdk_version=self.sdk_version,
            parts=parts_str,
        )
