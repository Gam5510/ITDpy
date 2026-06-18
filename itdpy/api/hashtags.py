from typing import Optional
import time
from ..api.base import BaseAPI
from ..models import HashtagPosts, TrendingHashtagsResponse, Post


class HashtagsAPI(BaseAPI):

    def trending(self, *, limit: int = 10) -> TrendingHashtagsResponse:
        response = self._get("hashtags/trending", params={"limit": limit})
        data = response.json()
        if isinstance(data, dict) and "data" in data:
            data = data["data"]
        return TrendingHashtagsResponse.from_data(data)

    def get_posts(
        self,
        hashtag: str,
        *,
        limit: int = 20,
        cursor: Optional[str] = None,
    ) -> HashtagPosts:
        params: dict = {"limit": limit}
        if cursor:
            params["cursor"] = cursor

        response = self._get(f"hashtags/{hashtag}/posts", params=params)
        return HashtagPosts.from_data(response.json())
    
    def get_all_posts(
        self,
        hashtag: str,
        *,
        limit: Optional[int] = None,
        delay: Optional[float] = 2.5
    ):
        

        if limit is None:
            posts = self.get_posts(hashtag=hashtag, limit=20)
            limit = posts.hashtag.posts_count
        elif limit <= 0:
            return HashtagPosts([], hashtag=hashtag, pagination=None)

        items: list[Post] = []
        seen_ids: set[str] = set()
        seen_cursors: set = set()
        cursor = None
        has_more = True

        while has_more and len(items) < limit:
            if cursor in seen_cursors:
                break
            seen_cursors.add(cursor)

            batch_limit = min(50, limit - len(items))
            time.sleep(delay)
            page = self.get_posts(
                hashtag=hashtag,
                limit=batch_limit,
                cursor=cursor,
            )
            new_items = page.to_list()

            if not new_items:
                break

            for post in new_items:
                if post.id not in seen_ids:
                    items.append(post)
                    seen_ids.add(post.id)

            new_cursor = page.pagination.cursor
            if new_cursor == cursor:
                break
            cursor = new_cursor
            has_more = page.pagination.has_more

        return HashtagPosts(items[:limit], hashtag=hashtag, pagination=page.pagination)
