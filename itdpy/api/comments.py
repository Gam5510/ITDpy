from typing import List, Optional

from ..api.base import BaseAPI
from ..enums import CommentSort
from ..models import Comment, CommentsList, CommentUpdate


class CommentsAPI(BaseAPI):
    @staticmethod
    def _unwrap_data(payload: dict | list) -> dict | list:
        if isinstance(payload, dict) and "data" in payload:
            return payload["data"]
        return payload

    def list(
        self,
        post_id: str,
        *,
        limit: int = 20,
        sort: CommentSort | str = CommentSort.POPULAR,
        cursor: Optional[str] = None,
    ) -> CommentsList:
        params = {"limit": limit, "sort": sort.value}
        if cursor is not None:
            params["cursor"] = cursor

        response = self._get(f"posts/{post_id}/comments", params=params)
        return CommentsList.from_data(response.json())

    def list_replies(
        self,
        comment_id: str,
        *,
        limit: int = 20,
        sort: CommentSort | str = CommentSort.NEWEST,
        cursor: Optional[str] = None,
    ) -> CommentsList:
        params = {"limit": limit, "sort": sort.value}
        if cursor is not None:
            params["cursor"] = cursor

        response = self._get(f"comments/{comment_id}/replies", params=params)
        return CommentsList.from_data(response.json())

    def get_replies(
        self,
        comment_id: str,
        *,
        limit: int = 20,
        sort: CommentSort | str = CommentSort.NEWEST,
        cursor: Optional[str] = None,
    ) -> CommentsList:
        return self.list_replies(comment_id, limit=limit, sort=sort, cursor=cursor)

    def list_all(
        self,
        post_id: str,
        *,
        limit: int = 50,
        sort: CommentSort | str = CommentSort.POPULAR,
    ) -> CommentsList:
        if limit <= 0:
            return CommentsList([], total=0, next_cursor=None, has_more=False)

        items: list[Comment] = []
        cursor: Optional[str] = None
        total: Optional[int] = None
        has_more = True

        while has_more and len(items) < limit:
            batch_limit = min(50, limit - len(items))
            page = self.list(post_id, limit=batch_limit, sort=sort, cursor=cursor)
            items.extend(page.to_list())
            total = page.total
            cursor = page.next_cursor
            has_more = page.has_more

            if len(page) == 0:
                break

        return CommentsList(
            items[:limit],
            total=total,
            next_cursor=cursor,
            has_more=has_more and len(items) >= limit,
        )

    def create(
        self,
        post_id: str,
        *,
        content: str,
        attachment_ids: Optional[List[str]] = None,
    ) -> Comment:
        payload = {
            "content": content,
            "attachmentIds": attachment_ids or [],
        }
        response = self._post(f"posts/{post_id}/comments", json=payload)
        return Comment.model_validate(self._unwrap_data(response.json()))

    def reply(
        self,
        comment_id: str,
        *,
        content: str,
        attachment_ids: Optional[List[str]] = None,
    ) -> Comment:
        payload = {
            "content": content,
            "attachmentIds": attachment_ids or [],
        }
        response = self._post(f"comments/{comment_id}/replies", json=payload)
        return Comment.model_validate(self._unwrap_data(response.json()))

    def delete(self, comment_id: str) -> None:
        self._delete(f"comments/{comment_id}")

    def like(self, comment_id: str) -> None:
        self._post(f"comments/{comment_id}/like")

    def unlike(self, comment_id: str) -> None:
        self._delete(f"comments/{comment_id}/like")

    def update(
        self,
        comment_id: str,
        content: str,
    ) -> CommentUpdate:
        payload = {"content": content}
        response = self._patch(f"comments/{comment_id}", json=payload)
        return CommentUpdate.model_validate(self._unwrap_data(response.json()))
