from ..api.base import BaseAPI
from ..models import Search, SearchHashtagsResponse, SearchUsersResponse

class SearchAPI(BaseAPI):
    def all(
        self,
        query: str,
        *,
        user_limit: int = 5,
        hashtag_limit: int = 5,
    ) -> Search:
        params = {
            "q": query,
            "userLimit": user_limit,
            "hashtagLimit": hashtag_limit,
        }
        response = self._get("search", params=params)
        return Search.model_validate(response.json())
    
    def users(self, query: str, *, limit: int = 10) -> SearchUsersResponse:
        params = {"q": query, "userLimit": limit, "hashtagLimit": 1}
        response = self._get("search", params=params)
        search = Search.model_validate(response.json())
        return SearchUsersResponse(items=search.users[:limit])
    
    def hashtags(self, query: str, *, limit: int = 10) -> SearchHashtagsResponse:
        params = {"q": query, "userLimit": 1, "hashtagLimit": limit}
        response = self._get("search", params=params)
        search = Search.model_validate(response.json())
        return SearchHashtagsResponse(items=search.hashtags[:limit])
