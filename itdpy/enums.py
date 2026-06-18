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
    FOLLOW_REQUEST = "follow_request"
    FOLLOW_ACCEPTED = "follow_accepted"
    COMMENT_LIKE = "comment_reaction"
    COMMENT_MENTION = "comment_mention"
    MENTION = "mention"
    WALL_POST = "wall_post"


class NotificationTargetType(str, Enum):
    POST = "post"


class InteractionType(int, Enum):
    PHOTO_OPEN = 1
    VIDEO_PROGRESS = 2


class ViewSource(int, Enum):
    FEED_GLOBAL = 1
    FEED_FOLLOWING = 2
    FEED_CLAN = 3
    PROFILE = 4
    HASHTAG = 5
    POST_PAGE = 6
    LINK = 7
    SEARCH = 8


class ViewReason(int, Enum):
    NORMAL = 0
    BLUR = 1
    HIDDEN = 2
    PAGE_HIDE = 3
    UNOBSERVE = 4
    THRESHOLD_MET = 5

class DeviceType(str, Enum):
    DESKTOP = "desktop"
    MOBILE = "mobile"
