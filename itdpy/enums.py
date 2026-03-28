from enum import Enum


class PostsTab(str, Enum):
    POPULAR = "popular"
    NEWEST = "newest"
    OLDEST = "oldest"
    FOLLOWING = "following"
    CLAN = "clan"


class UserPostSorting(str, Enum):
    NEW = "new"
    POPULAR = "popular"


class CommentSort(str, Enum):
    POPULAR = "popular"
    NEWEST = "newest"
    OLDEST = "oldest"


class AccessType(str, Enum):
    NOBODY = "nobody"
    MUTUAL = "mutual"
    FOLLOWERS = "followers"
    EVERYONE = "everyone"


class ReportTargetType(str, Enum):
    POST = "post"
    USER = "user"
    COMMENT = "comment"


class ReportReason(str, Enum):
    SPAM = "spam"
    VIOLENCE = "violence"
    HATE = "hate"
    ADULT = "adult"
    FRAUD = "fraud"
    OTHER = "other"


class SpanType(str, Enum):
    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"
    STRIKE = "strike"
    MONOSPACE = "monospace"
    SPOILER = "spoiler"
    QUOTE = "quote"
    LINK = "link"
    MENTION = "mention"
    HASHTAG = "hashtag"

class NotificationType(str, Enum):
    LIKE = "like"
    COMMENT = "comment"
    REPLY = "reply"
    REPOST = "repost"
    FOLLOW = "follow"
    WALL_POST = "wall_post"


class NotificationTargetType(str, Enum):
    POST = "post"

