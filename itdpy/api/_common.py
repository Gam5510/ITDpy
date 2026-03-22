from __future__ import annotations

from typing import Sequence
from urllib.parse import urlencode

def normalize_id_list(values: Sequence[str] | str | None) -> list[str]:
    if values is None:
        return []
    if isinstance(values, str):
        return [values]
    return [v for v in values if isinstance(v, str) and v]


def truthy_response_status(status_code: int) -> bool:
    return 200 <= status_code < 300


def build_query(params: dict[str, object]) -> str:
    clean = {k: v for k, v in params.items() if v is not None}
    return urlencode(clean)


__all__ = [
    "build_query",
    "normalize_id_list",
    "truthy_response_status",
]
