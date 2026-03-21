from __future__ import annotations

from ..api.base import BaseAPI
from ..models import HashtagPosts, Portal, Search, TopClansResponse, TrendingHashtagsResponse, WhoToFollow


class DiscoveryAPI(BaseAPI):
    def get_top_clans(self) -> TopClansResponse:
        response = self._get("/users/stats/top-clans")
        return TopClansResponse.from_data(response.json())

    def who_to_follow(self) -> WhoToFollow:
        response = self._get("/users/suggestions/who-to-follow")
        return WhoToFollow.from_data(response.json())

    def search_hashtags(self, name: str, limit: int = 20) -> HashtagPosts:
        response = self._get(f"/hashtags/{name}/posts", params={"limit": limit})
        return HashtagPosts.from_data(response.json())

    def search(self, query: str, user_limit: int = 5, hashtag_limit: int = 5) -> Search:
        response = self._get(
            "/search",
            params={"q": query, "userLimit": user_limit, "hashtagLimit": hashtag_limit},
        )
        return Search.model_validate(response.json())

    def get_trending_hashtags(self, limit: int = 10) -> TrendingHashtagsResponse:
        response = self._get("/hashtags/trending", params={"limit": limit})
        data = response.json()
        if isinstance(data, dict) and "data" in data:
            data = data["data"]
        return TrendingHashtagsResponse.from_data(data)

    def portal(self) -> Portal:
        response = self._get("/v1/portal")
        data = response.json()
        if isinstance(data, dict) and "data" in data:
            data = data["data"]
        return Portal.model_validate(data)
