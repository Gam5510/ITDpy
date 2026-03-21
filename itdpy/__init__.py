"""
itdpy - Production-ready Python SDK for ITD API
"""

__version__ = "1.0.0"

from .client import ITDClient
from .config import Config
from .enums import (
    PostsTab,
    UserPostSorting,
    CommentSort,
    AccessType,
    ReportReason,
    ReportTargetType,
)
from .exceptions import (
    ITDError,
    APIError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
)
from .streaming import NotificationStream, StreamEvent
from .models import (
    Post,
    User,
    Comment,
    Notification,
    Portal,
    FollowStatusItem,
    PostViewResponse,
)

__all__ = [
    "ITDClient",
    "Config",
    "PostsTab",
    "UserPostSorting",
    "CommentSort",
    "AccessType",
    "ReportReason",
    "ReportTargetType",
    "ITDError",
    "APIError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "NotificationStream",
    "StreamEvent",
    "Post",
    "User",
    "Comment",
    "Notification",
    "Portal",
    "FollowStatusItem",
    "PostViewResponse",
]
