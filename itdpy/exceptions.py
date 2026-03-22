class ITDError(Exception):
    pass

class APIError(ITDError):
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class AuthenticationError(APIError):
    pass

class NotFoundError(APIError):
    pass

class ValidationError(APIError):
    pass

class RateLimitError(APIError):
    def __init__(self, message: str, retry_after: int = 60):
        super().__init__(message, status_code=429)
        self.retry_after = retry_after

class NetworkError(ITDError):
    pass

class ContentError(ITDError):
    pass

class BlockedUserError(ITDError):
    pass

class ITDAttributeError(Exception):
    pass