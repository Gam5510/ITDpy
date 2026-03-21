from typing import Optional, Sequence

from ..api.base import BaseAPI
from ..enums import AccessType
from ..models import FollowStatusItem, NotificationSettings, PrivacySettings, User, UsersList


class UsersAPI(BaseAPI):
    def me(self) -> User:
        response = self._get("users/me")
        return User.model_validate(response.json())

    def get(self, username: str) -> User:
        response = self._get(f"users/{username}")
        return User.model_validate(response.json())

    def follow(self, username: str) -> None:
        self._post(f"users/{username}/follow")

    def unfollow(self, username: str) -> None:
        self._delete(f"users/{username}/follow")

    def get_followers(
        self,
        user_id: str,
        *,
        limit: int = 20,
        page: int = 1,
    ) -> UsersList:
        params = {"limit": limit, "page": page}
        response = self._get(f"users/{user_id}/followers", params=params)
        return UsersList.from_data(response.json())

    def get_following(
        self,
        user_id: str,
        *,
        limit: int = 20,
        page: int = 1,
    ) -> UsersList:
        params = {"limit": limit, "page": page}
        response = self._get(f"users/{user_id}/following", params=params)
        return UsersList.from_data(response.json())

    def update_profile(
        self,
        *,
        display_name: Optional[str] = None,
        username: Optional[str] = None,
        bio: Optional[str] = None,
        banner_id: Optional[str] = None,
    ) -> User:
        payload = {}
        if display_name is not None:
            payload["displayName"] = display_name
        if username is not None:
            payload["username"] = username
        if bio is not None:
            payload["bio"] = bio
        if banner_id is not None:
            payload["bannerId"] = banner_id

        response = self._put("users/me", json=payload)
        return User.model_validate(response.json())

    def update_privacy(
        self,
        *,
        is_private: Optional[bool] = None,
        wall_access: Optional[AccessType] = None,
        likes_visibility: Optional[AccessType] = None,
        show_last_seen: Optional[bool] = None,
    ) -> PrivacySettings:
        payload = {}
        if is_private is not None:
            payload["isPrivate"] = is_private

        if wall_access is not None:
            payload["wallAccess"] = wall_access.value

        if likes_visibility is not None:
            payload["likesVisibility"] = likes_visibility.value

        if show_last_seen is not None:
            payload["showLastSeen"] = show_last_seen

        response = self._put("users/me/privacy", json=payload)
        return PrivacySettings.model_validate(response.json())

    def update_notification_settings(
        self,
        *,
        enabled: Optional[bool] = None,
        comments: Optional[bool] = None,
        follows: Optional[bool] = None,
        likes: Optional[bool] = None,
        mentions: Optional[bool] = None,
        sound: Optional[bool] = None,
        wall_posts: Optional[bool] = None,
    ) -> NotificationSettings:
        payload: dict[str, object] = {}

        if enabled is not None:
            payload["enabled"] = enabled
        if comments is not None:
            payload["comments"] = comments
        if follows is not None:
            payload["follows"] = follows
        if likes is not None:
            payload["likes"] = likes
        if mentions is not None:
            payload["mentions"] = mentions
        if sound is not None:
            payload["sound"] = sound
        if wall_posts is not None:
            payload["wallPosts"] = wall_posts

        if not payload:
            raise ValueError("No notification fields provided to update")

        response = self._put("/notifications/settings", json=payload)
        return NotificationSettings.model_validate(response.json())

    def block(self, username: str) -> None:
        self._post(f"users/{username}/block")

    def unblock(self, username: str) -> None:
        self._delete(f"users/{username}/block")

    def follow_status(self, user_ids: Sequence[str]) -> list[FollowStatusItem]:
        response = self._post("users/follow-status", json={"userIds": list(user_ids)})
        data = response.json()

        if isinstance(data, dict) and "data" in data:
            data = data["data"]

        if isinstance(data, dict):
            if any(isinstance(value, bool) for value in data.values()):
                items = [
                    {
                        "id": user_id,
                        "isFollowing": is_following
                    }
                    for user_id, is_following in data.items()
                ]
            else:
                items = data.get("items") or data.get("users") or data.get("statuses") or []
        else:
            items = data

        return [FollowStatusItem.model_validate(item) for item in items]
