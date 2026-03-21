# 46_error_handling.py
# Обработка типовых ошибок

from itdpy import (
    APIError,
    AuthenticationError,
    ITDClient,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
import time

client = ITDClient(refresh_token="токен")

try:
    client.posts.get("invalid_post_id")
except NotFoundError:
    print("Post not found")
except ValidationError as e:
    print("Validation:", e.message)
except APIError as e:
    print("API error:", e.message)
except AuthenticationError as e:
    print("Auth error:", e.message)
except RateLimitError as e:
    print("Rarelimit error:", e.message)
    time.sleep(e.retry_after)
client.close()
