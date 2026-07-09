import json
import os
import tempfile
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


def default_profiles_path() -> Path:
    return Path.home() / ".itdpy" / "profiles.json"


@dataclass
class Profile:
    name: str
    refresh_token: str
    access_token: Optional[str] = None
    access_expires_at: Optional[float] = None
    email: Optional[str] = None
    user_id: Optional[str] = None
    device_id: Optional[str] = None
    updated_at: float = field(default_factory=time.time)

    def is_access_token_valid(self, leeway: float = 30) -> bool:
        if not self.access_token or not self.access_expires_at:
            return False
        return time.time() < (self.access_expires_at - leeway)


class ProfileStore:
    def __init__(self, path: Optional[str] = None):
        self.path = Path(path) if path else default_profiles_path()

    def _read_all(self) -> dict:
        if not self.path.exists():
            return {}
        with open(self.path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def _write_all(self, data: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(
            dir=str(self.path.parent), prefix=".profiles-", suffix=".tmp",
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, self.path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        try:
            os.chmod(self.path, 0o600)
        except OSError:
            pass

    def load(self, name: str) -> Optional[Profile]:
        data = self._read_all().get(name)
        if not data:
            return None
        return Profile(name=name, **data)

    def save(self, profile: Profile) -> None:
        data = self._read_all()
        entry = asdict(profile)
        entry.pop("name")
        data[profile.name] = entry
        self._write_all(data)

    def touch(self, name: str, **fields) -> None:
        data = self._read_all()
        entry = data.get(name, {})
        entry.update(fields)
        entry["updated_at"] = time.time()
        data[name] = entry
        self._write_all(data)

    def delete(self, name: str) -> None:
        data = self._read_all()
        if name in data:
            del data[name]
            self._write_all(data)

    def list(self) -> list:
        return list(self._read_all().keys())
