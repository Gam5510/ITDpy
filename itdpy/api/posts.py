from typing import List, Optional

from ..api.base import BaseAPI
from ..enums import PostsTab, UserPostSorting
from ..formatting import format_html, format_markdown
from ..models import LikesCountResponse, Poll, Post, PostsList, PostUpdate, PostViewResponse, User


class PostsAPI(BaseAPI):
    @staticmethod
    def _unwrap_data(payload):
        if isinstance(payload, dict) and "data" in payload:
            return payload["data"]
        return payload

    @staticmethod
    def _serialize_poll(poll: dict | Poll | object) -> dict:
        if hasattr(poll, "to_request_dict") and callable(poll.to_request_dict):
            data = poll.to_request_dict()
        elif hasattr(poll, "to_dict") and callable(poll.to_dict):
            data = poll.to_dict()
        elif isinstance(poll, dict):
            data = dict(poll)
        else:
            raise TypeError("poll must be a dict or Poll-like object with to_dict()")

        options = data.get("options", [])
        normalized_options: list[dict[str, str]] = []
        for option in options:
            if isinstance(option, str):
                text = option
            elif isinstance(option, dict):
                text = str(option.get("text", ""))
            elif hasattr(option, "text"):
                text = str(option.text)
            else:
                text = str(option)

            normalized_options.append({"text": text})

        data["options"] = normalized_options
        return data

    def list(
        self,
        *,
        limit: int = 20,
        tab: PostsTab = PostsTab.POPULAR,
        cursor: Optional[int] = None,
    ) -> PostsList:
        params = {"limit": limit, "tab": tab.value}
        if cursor is not None:
            params["cursor"] = cursor

        response = self._get("posts", params=params)
        return PostsList.from_data(response.json())

    def list_all(
        self,
        *,
        limit: int = 50,
        tab: PostsTab = PostsTab.POPULAR,
    ) -> PostsList:
        if limit <= 0:
            return PostsList([], cursor=None, has_more=False)

        items: list[Post] = []
        cursor: Optional[int] = None
        has_more = True

        while has_more and len(items) < limit:
            batch_limit = min(50, limit - len(items))
            page = self.list(limit=batch_limit, tab=tab, cursor=cursor)
            items.extend(page.to_list())
            cursor = page.cursor
            has_more = page.has_more

        return PostsList(items[:limit], cursor=cursor, has_more=has_more and len(items) >= limit)

    def get(self, post_id: str) -> Post:
        response = self._get(f"posts/{post_id}")
        return Post.model_validate(self._unwrap_data(response.json()))

    def create(
        self,
        *,
        content: str = "",
        attachment_ids: Optional[List[str]] = None,
        wall_recipient_id: Optional[str] = None,
        poll: Optional[dict | Poll] = None,
        parse_html: bool = False,
        parse_md: bool = False,
    ) -> Post:
        payload = {
            "content": content,
            "attachmentIds": attachment_ids or [],
        }

        if content:
            if parse_md:
                formatted = format_markdown(content)
                payload["content"] = formatted["content"]
                payload["spans"] = formatted["spans"]
            elif parse_html:
                formatted = format_html(content)
                payload["content"] = formatted["content"]
                payload["spans"] = formatted["spans"]

        if wall_recipient_id:
            payload["wallRecipientId"] = wall_recipient_id

        if poll:
            payload["poll"] = self._serialize_poll(poll)

        response = self._post("posts", json=payload)
        return Post.model_validate(self._unwrap_data(response.json()))

    def post_to_wall(
        self,
        *,
        content: str,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
        attachment_ids: Optional[List[str]] = None,
        poll: Optional[dict | Poll] = None,
        parse_html: bool = False,
        parse_md: bool = False,
    ) -> Post:
        if not username and not user_id:
            raise ValueError("username or user_id is required")

        wall_recipient_id = user_id
        if wall_recipient_id is None:
            response = self._get(f"users/{username}")
            user = User.model_validate(response.json())
            if not user.id:
                raise ValueError(f"Failed to resolve recipient id for @{username}")
            wall_recipient_id = user.id

        return self.create(
            content=content,
            attachment_ids=attachment_ids,
            wall_recipient_id=wall_recipient_id,
            poll=poll,
            parse_html=parse_html,
            parse_md=parse_md,
        )

    def update(
        self,
        post_id: str,
        *,
        content: str,
        parse_html: bool = False,
        parse_md: bool = False,
    ) -> PostUpdate:
        payload = {"content": content}

        if parse_md:
            formatted = format_markdown(content)
            payload["content"] = formatted["content"]
            payload["spans"] = formatted["spans"]
        elif parse_html:
            formatted = format_html(content)
            payload["content"] = formatted["content"]
            payload["spans"] = formatted["spans"]

        response = self._put(f"posts/{post_id}", json=payload)
        return PostUpdate.model_validate(self._unwrap_data(response.json()))

    def delete(self, post_id: str) -> None:
        self._delete(f"posts/{post_id}")

    def like(self, post_id: str) -> LikesCountResponse:
        response = self._post(f"posts/{post_id}/like")
        return LikesCountResponse.model_validate(response.json())

    def unlike(self, post_id: str) -> LikesCountResponse:
        response = self._delete(f"posts/{post_id}/like")
        return LikesCountResponse.model_validate(response.json())

    def repost(self, post_id: str, content: Optional[str] = None) -> Post:
        payload = {"content": content} if content else {}
        response = self._post(f"posts/{post_id}/repost", json=payload)
        return Post.model_validate(self._unwrap_data(response.json()))

    def get_user_posts(
        self,
        username: str,
        *,
        limit: int = 20,
        sort: UserPostSorting = UserPostSorting.NEW,
        cursor: Optional[str] = None,
    ) -> PostsList:
        params = {"limit": limit, "sort": sort.value}
        if cursor:
            params["cursor"] = cursor

        response = self._get(f"posts/user/{username}", params=params)
        return PostsList.from_data(response.json())

    def get_all_user_posts(
        self,
        username: str,
        *,
        limit: int = 50,
        sort: UserPostSorting = UserPostSorting.NEW,
    ) -> PostsList:
        if limit <= 0:
            return PostsList([], cursor=None, has_more=False)

        items: list[Post] = []
        cursor: Optional[str] = None
        has_more = True

        while has_more and len(items) < limit:
            batch_limit = min(50, limit - len(items))
            page = self.get_user_posts(username, limit=batch_limit, sort=sort, cursor=cursor)
            items.extend(page.to_list())
            has_more = page.has_more
            cursor = page.cursor

        return PostsList(items[:limit], cursor=cursor, has_more=has_more and len(items) >= limit)

    def vote(self, post_id: str, option_ids: str | List[str]) -> Poll:
        if isinstance(option_ids, str):
            option_ids = [option_ids]

        payload = {"optionIds": option_ids}
        response = self._post(f"posts/{post_id}/poll/vote", json=payload)
        return Poll.model_validate(self._unwrap_data(response.json()))

    def view(self, post_id: str) -> PostViewResponse:
        response = self._post(f"posts/{post_id}/view")
        if response.status_code in (200, 204):
            return PostViewResponse(viewed=True)
        return PostViewResponse.model_validate(response.json())

    def view_many(self, post_ids: List[str]) -> dict[str, bool]:
        return {post_id: self.view(post_id).viewed for post_id in post_ids}
