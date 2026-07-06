class ITDError(Exception):
    """Base exception for all ITDpy errors."""


class APIError(ITDError):
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class AuthenticationError(APIError):
    """Authentication failed (401)."""


class InvalidCredentialsError(AuthenticationError):
    """Email or password is incorrect (login-with-password flow)."""


class TurnstileTimeoutError(AuthenticationError):
    """Cloudflare Turnstile challenge was not solved in time."""


class BrowserNotAvailableError(AuthenticationError):
    """DrissionPage/browser is not installed or could not be launched."""


class SessionNotFoundError(AuthenticationError):
    """Invalid or missing refresh token."""


class SessionExpiredError(AuthenticationError):
    """Session has expired."""


class SessionRevokedError(AuthenticationError):
    """Session was revoked."""


class AccessTokenExpiredError(AuthenticationError):
    """Access token expired."""

class NotFoundError(APIError):
    """Resource not found (404)."""


class ValidationError(APIError):
    """Request validation failed (422)."""


class ForbiddenError(APIError):
    """Action is forbidden (403)."""


class RateLimitError(APIError):
    def __init__(self, message: str, retry_after: int = 60):
        super().__init__(message, status_code=429)
        self.retry_after = retry_after

class NetworkError(ITDError):
    """Network-level error."""

class ContentError(ITDError):
    """Content-related error."""


class BannedWordError(ContentError):
    """Content contains a prohibited word."""


class ModerationFailedError(ContentError):
    """Content failed moderation."""

class BlockedUserError(ITDError):
    """Target user is blocked or has blocked you."""


class CantFollowYourselfError(ITDError):
    """Cannot follow yourself."""


class CantRepostYourselfError(ITDError):
    """Cannot repost your own post."""


class CantBlockYourselfError(ITDError):
    """Cannot block yourself."""


class UsernameTakenError(ValidationError):
    """Username is already taken."""


class TargetUserBannedError(ITDError):
    """Target user has been deactivated."""


class AccountBannedError(AuthenticationError):
    """Your account has been deactivated."""

class AlreadyRepostedError(ITDError):
    """Post already reposted."""


class EditExpiredError(ITDError):
    """Edit window expired (48h)."""


class NotPinnedError(ITDError):
    """Post is not pinned."""

class OptionsNotBelongError(ITDError):
    """Options do not belong to this poll."""


class NotMultipleChoiceError(ITDError):
    """This poll does not allow multiple choices."""

class InvalidFileTypeError(ITDError):
    """Invalid file type."""


class UploadError(ITDError):
    """File upload failed."""

class RequiresSubscriptionError(ForbiddenError):
    """Feature requires active НУКСТА subscription."""


class RequiresVerificationError(ForbiddenError):
    """Feature requires account verification."""

class AlreadyReportedError(ITDError):
    """Object already reported."""

class AlreadyFollowingError(ITDError):
    """Already following this user."""


class AlreadyBlockedError(ITDError):
    """User already blocked."""


class NotBlockedError(ITDError):
    """User is not blocked."""

class AlreadyDeletedError(ITDError):
    """Account/resource already deleted."""


class NotDeletedError(ITDError):
    """Account/resource is not deleted."""


class ProfileRequiredError(ITDError):
    """Profile must be created first."""


class ITDAttributeError(Exception):
    """Attribute not found (usually removed/renamed API)."""


ITDException = ITDError
