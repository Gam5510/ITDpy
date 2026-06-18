from typing import Dict, List, Optional

from ..api.base import BaseAPI
from ..enums import PostsTab, UserPostSorting
from ..formatting import format_html, format_markdown
from ..models import LikesCountResponse, Poll, Post, PostsList, PostUpdate, PostViewResponse, User
from ..enums import InteractionType, ViewReason, ViewSource
import uuid

class PostsAPI(BaseAPI):
    @staticmethod
    def _unwrap_data(payload):
        if isinstance(payload, dict) and "data" in payload:
            return payload["data"]
        return payload

    @staticmethod
    def _serialize_poll(poll: "dict | Poll | object") -> dict:
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
        tab: "PostsTab | str" = PostsTab.POPULAR,
        cursor: Optional[int] = None,
    ) -> PostsList:
        tab_value = tab.value if isinstance(tab, PostsTab) else str(tab)
        params: dict = {"limit": limit, "tab": tab_value}
        if cursor is not None:
            params["cursor"] = cursor

        response = self._get("posts", params=params)
        return PostsList.from_data(response.json())

    def list_all(
        self,
        *,
        limit: int = 50,
        tab: "PostsTab | str" = PostsTab.POPULAR,
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
        poll: "Optional[dict | Poll]" = None,
        parse_html: bool = False,
        parse_md: bool = False,
    ) -> Post:
        payload: dict = {
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
        poll: "Optional[dict | Poll]" = None,
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
        payload: dict = {"content": content}

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

    def restore(self, post_id: str) -> None:
        self._post(f"posts/{post_id}/restore")

    def pin(self, post_id: str) -> None:
        self._post(f"posts/{post_id}/pin")

    def unpin(self, post_id: str) -> None:
        self._delete(f"posts/{post_id}/pin")

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
        sort: "UserPostSorting | str" = UserPostSorting.NEW,
        cursor: Optional[str] = None,
        pinned_post_id: Optional[str] = None,
    ) -> PostsList:
        params: dict = {}
        if limit:
            params["limit"] = min(max(limit, 1), 50)
        else:
            params["limit"] = 20

        params["sort"] = sort.value if isinstance(sort, UserPostSorting) else str(sort)

        if cursor:
            params["cursor"] = cursor
        if pinned_post_id:
            params["pinnedPostId"] = pinned_post_id

        response = self._get(f"posts/user/{username}", params=params)
        return PostsList.from_data(response.json())

    def get_all_user_posts(
        self,
        username: str,
        *,
        limit: Optional[int] = None,
        sort: "UserPostSorting | str" = UserPostSorting.NEW,
    ) -> PostsList:
        user = self._get(f"users/{username}").json()

        if limit is None:
            limit = user.get("postsCount", 0)
        elif limit <= 0:
            return PostsList([], cursor=None, has_more=False)

        items: list[Post] = []
        seen_ids: set[str] = set()
        seen_cursors: set = set()
        pinned_id = user.get("pinnedPostId")
        cursor = None
        has_more = True

        while has_more and len(items) < limit:
            if cursor in seen_cursors:
                break
            seen_cursors.add(cursor)

            batch_limit = min(50, limit - len(items))
            page = self.get_user_posts(
                username,
                limit=batch_limit,
                sort=sort,
                cursor=cursor,
                pinned_post_id=pinned_id,
            )
            new_items = page.to_list()

            if not new_items:
                break

            for post in new_items:
                if post.id == pinned_id:
                    continue
                if post.id not in seen_ids:
                    items.append(post)
                    seen_ids.add(post.id)

            new_cursor = new_items[-1].created_at
            if new_cursor == cursor:
                break
            cursor = new_cursor
            has_more = page.has_more

        return PostsList(items[:limit], cursor=cursor, has_more=has_more)

    def get_liked(
        self,
        username_or_id: str,
        *,
        limit: int = 20,
        cursor: Optional[str] = None,
    ) -> PostsList:
        params: dict = {"limit": limit}
        if cursor:
            params["cursor"] = cursor

        response = self._get(f"posts/user/{username_or_id}/liked", params=params)
        return PostsList.from_data(response.json())


    def get_stats(self, post_ids: List[str]) -> List[dict]:
        response = self._post("posts/stats", json={"ids": post_ids})
        data = response.json()
        if isinstance(data, dict):
            return data.get("data", data.get("stats", []))
        if isinstance(data, list):
            return data
        return []

    def vote(self, post_id: str, option_ids: "str | List[str]") -> Poll:
        if isinstance(option_ids, str):
            option_ids = [option_ids]

        response = self._post(f"posts/{post_id}/poll/vote", json={"optionIds": option_ids})
        data = response.json()
        if isinstance(data, dict) and "data" in data:
            data = data["data"]
        return Poll.model_validate(data)

    def _make_sid(self) -> str:
        return str(uuid.uuid4())

    def _send_views(self, objects: list, session_id: Optional[str] = None) -> None:
        sid = session_id or self._make_sid()
        self._post("v1/i", json={"e": objects, "sid": sid})

    def _send_interactions(self, objects: list, session_id: Optional[str] = None) -> None:
        sid = session_id or self._make_sid()
        self._post("v1/x", json={"e": objects, "sid": sid})

    def view_post(
        self,
        post_id: str,
        *,
        source: "ViewSource | int" = ViewSource.FEED_GLOBAL,
        reason: "ViewReason | int" = ViewReason.NORMAL,
        session_id: Optional[str] = None,
    ) -> None:
        source_val = source.value if isinstance(source, ViewSource) else int(source)
        reason_val = reason.value if isinstance(reason, ViewReason) else int(reason)

        event = {
            "id": post_id,
            "s": source_val,
            "r": reason_val,
        }
        self._send_views([event], session_id=session_id)

    def interaction(
        self,
        post_id: str,
        interaction_type: "InteractionType | int",
        *,
        session_id: Optional[str] = None,
    ) -> None:
        type_val = interaction_type.value if isinstance(interaction_type, InteractionType) else int(interaction_type)

        event = {
            "id": post_id,
            "t": type_val,
        }
        self._send_interactions([event], session_id=session_id)

    def view_many(
        self,
        post_ids: list,
        *,
        source: "ViewSource | int" = ViewSource.FEED_GLOBAL,
        reason: "ViewReason | int" = ViewReason.NORMAL,
    ) -> None:
        source_val = source.value if isinstance(source, ViewSource) else int(source)
        reason_val = reason.value if isinstance(reason, ViewReason) else int(reason)

        events = [{"id": pid, "s": source_val, "r": reason_val} for pid in post_ids]
        sid = self._make_sid()
        self._send_views(events, session_id=sid)
