from __future__ import annotations

import json
from typing import Generic, Iterable, Iterator, Sequence, TypeVar

from pydantic import BaseModel, ConfigDict, Field

ModelT = TypeVar("ModelT", bound="ITDBaseModel")
T = TypeVar("T")


class ITDBaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
    )

    def __getattribute__(self, name: str):
        value = super().__getattribute__(name)
        if isinstance(value, list) and not isinstance(value, BaseList):
            return BaseList(value)
        return value

    def __getitem__(self, key: str):
        if hasattr(self, key):
            return getattr(self, key)

        for field_name, field_info in self.__class__.model_fields.items():
            if field_name == key:
                return getattr(self, field_name)
            if field_info.alias == key:
                return getattr(self, field_name)

        raise KeyError(key)

    def get(self, key: str, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def to_dict(self, **kwargs) -> dict[str, object]:
        kwargs.setdefault("by_alias", True)
        kwargs.setdefault("exclude_none", True)
        return self.model_dump(**kwargs)

    def to_json(self, **kwargs) -> str:
        kwargs.setdefault("by_alias", True)
        kwargs.setdefault("exclude_none", True)
        return self.model_dump_json(**kwargs)

    def to_request_dict(self) -> dict[str, object]:
        return self.to_dict()

    def copy(self, **kwargs):
        return self.model_copy(**kwargs)

    def __repr__(self) -> str:
        preview = ", ".join(
            f"{name}={value!r}"
            for name, value in list(self.__dict__.items())[:3]
        )
        return f"{self.__class__.__name__}({preview})"

    def __str__(self) -> str:
        return json.dumps(
            self.to_dict(by_alias=True),
            ensure_ascii=False,
            default=str
        )

    def __iter__(self):
        yield from self.to_dict().items()


class BaseList(Generic[T]):
    def __init__(self, items: Iterable[T] | None = None):
        if items is None:
            self.items = []
        elif isinstance(items, list):
            self.items = items
        else:
            self.items = list(items)

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

    def __getitem__(self, index: int | slice) -> T | list[T]:
        return self.items[index]

    def get(self, index: int, default=None):
        try:
            return self.items[index]
        except IndexError:
            return default

    def __len__(self) -> int:
        return len(self.items)

    def append(self, item: T) -> None:
        self.items.append(item)

    def extend(self, items: Iterable[T]) -> None:
        self.items.extend(items)

    def first(self) -> T | None:
        return self.items[0] if self.items else None

    def to_list(self) -> list[T]:
        return list(self.items)

    def to_dict(self, **kwargs) -> list[object]:
        kwargs.setdefault("by_alias", True)
        kwargs.setdefault("exclude_none", True)
        result: list[object] = []

        for item in self.items:
            if hasattr(item, "to_dict"):
                result.append(item.to_dict(**kwargs))
            else:
                result.append(item)

        return result

    def to_request_dict(self) -> list[object]:
        result: list[object] = []

        for item in self.items:
            if hasattr(item, "to_request_dict"):
                result.append(item.to_request_dict())
            elif hasattr(item, "to_dict"):
                result.append(item.to_dict())
            else:
                result.append(item)

        return result

    def to_json(self, **kwargs) -> str:
        kwargs.setdefault("ensure_ascii", False)
        return json.dumps(self.to_dict(), **kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(items={len(self.items)})"

    def __str__(self) -> str:
        return self.to_json()


class StatusResponse(ITDBaseModel):
    success: bool = True


class LikesCountResponse(ITDBaseModel):
    likes_count: int = Field(alias="likesCount")


def parse_model(model: type[ModelT], data: dict[str, object] | ModelT) -> ModelT:
    if isinstance(data, model):
        return data
    return model.model_validate(data)


def parse_list(model: type[ModelT], data: Sequence[dict[str, object] | ModelT] | BaseList[ModelT]) -> BaseList[ModelT]:
    if isinstance(data, BaseList):
        return data
    return BaseList(parse_model(model, item) for item in data)
