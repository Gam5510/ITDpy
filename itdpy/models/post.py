from typing import TYPE_CHECKING, List, Optional

from pydantic import Field, field_validator

from .base import BaseList, ITDBaseModel, parse_list
from .pagination import Pagination
if TYPE_CHECKING:
    from .user import UserLite


class Span(ITDBaseModel):
    offset: int
    length: int
    type: str
    url: Optional[str] = None


class PollOption(ITDBaseModel):
    id: Optional[str] = None
    text: str
    position: int = 0
    votes_count: int = Field(0, alias="votesCount")


class Poll(ITDBaseModel):
    id: Optional[str] = None
    post_id: Optional[str] = Field(None, alias="postId")
    question: str
    options: List[PollOption]
    total_votes: int = Field(0, alias="totalVotes")
    has_voted: bool = Field(False, alias="hasVoted")
    voted_option_ids: List[str] = Field(default_factory=list, alias="votedOptionIds")
    multiple_choice: bool = Field(False, alias="multipleChoice")
    created_at: Optional[str] = Field(None, alias="createdAt")

    @field_validator("options", mode="before")
    @classmethod
    def convert_options(cls, value: List[object]) -> List[PollOption]:
        result: list[PollOption] = []

        for item in value:
            if isinstance(item, PollOption):
                result.append(item)
            elif isinstance(item, dict):
                result.append(PollOption.model_validate(item))
            else:
                result.append(PollOption(text=str(item)))

        return result

    def to_dict(self, **kwargs) -> dict[str, object]:
        kwargs.setdefault("by_alias", True)
        kwargs.setdefault("exclude_none", True)
        return self.model_dump(**kwargs)

    def to_request_dict(self) -> dict[str, object]:
        return {
            "question": self.question,
            "multipleChoice": self.multiple_choice,
            "options": [{"text": option.text} for option in self.options],
        }


class PollBuilder:
    def __init__(self, question: str):
        self._question = question
        self._options: list[str] = []
        self._multiple_choice = False

    def add(self, text: object) -> "PollBuilder":
        self._options.append(str(text))
        return self

    def multiple_choice(self, flag: bool) -> "PollBuilder":
        self._multiple_choice = flag
        return self

    def build(self) -> Poll:
        return Poll(
            question=self._question,
            options=self._options,
            multipleChoice=self._multiple_choice,
        )

    def to_dict(self, **kwargs) -> dict[str, object]:
        return self.build().to_dict(**kwargs)

    def to_json(self, **kwargs) -> str:
        return self.build().to_json(**kwargs)

    def to_request_dict(self) -> dict[str, object]:
        return self.build().to_request_dict()

    def get(self, key: str, default=None):
        return self.build().get(key, default)

    def __getitem__(self, key: str):
        return self.build()[key]

    def __repr__(self) -> str:
        return repr(self.build())

    def __str__(self) -> str:
        return str(self.build())


class Attachment(ITDBaseModel):
    id: str
    url: str
    type: str
    size: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None


class Post(ITDBaseModel):
    id: str
    content: Optional[str] = None
    spans: List[Span] = Field(default_factory=list)

    likes_count: int = Field(0, alias="likesCount")
    comments_count: int = Field(0, alias="commentsCount")
    reposts_count: int = Field(0, alias="repostsCount")
    views_count: int = Field(0, alias="viewsCount")

    is_liked: bool = Field(False, alias="isLiked")
    is_reposted: bool = Field(False, alias="isReposted")
    is_viewed: bool = Field(False, alias="isViewed")
    is_owner: bool = Field(False, alias="isOwner")
    is_pinned: bool = Field(False, alias="isPinned")

    created_at: str = Field(alias="createdAt")
    edited_at: Optional[str] = Field(None, alias="editedAt")

    author: Optional["UserLite"] = None
    attachments: List[Attachment] = Field(default_factory=list)
    poll: Optional[Poll] = None
    original_post: Optional["Post"] = Field(None, alias="originalPost")
    wall_recipient: Optional["UserLite"] = Field(None, alias="wallRecipient")
    wall_recipient_id: Optional[str] = Field(None, alias="wallRecipientId")
    dominant_emoji: Optional[str] = Field(None, alias="dominantEmoji")
    author_id: Optional[str] = Field(None, alias="authorId")


class PostsList(BaseList[Post]):
    def __init__(
        self,
        items: List[Post] | None = None,
        *,
        cursor: Optional[str | int] = None,
        has_more: bool = False,
    ):
        super().__init__(items)
        self.cursor = cursor
        self.has_more = has_more

    @classmethod
    def from_data(cls, data: dict | list) -> "PostsList":
        items = []
        cursor = None
        has_more = False

        if isinstance(data, dict):

            raw = data.get("data", [])

            if isinstance(raw, list):
                items = raw
            elif isinstance(raw, dict):
                items = raw.get("posts", []) 
            else:
                items = []
            pagination = Pagination.model_validate(raw.get("pagination", {}))
            cursor = pagination.cursor
            has_more = pagination.has_more

        elif isinstance(data, list):
            items = data

        return cls(
            parse_list(Post, items).to_list(),
            cursor=cursor,
            has_more=has_more,
        )


class PostUpdate(ITDBaseModel):
    id: str
    content: Optional[str] = None
    spans: list[Span] = Field(default_factory=list)

    updated_at: str = Field(..., alias="updatedAt")


PostsResponse = PostsList
