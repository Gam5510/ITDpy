import difflib

SUGGESTIONS = {
    # low-level client
    "get": "client._request_handler.request('GET', endpoint)  # низкоуровневый вызов",
    "post": "client._request_handler.request('POST', endpoint)  # низкоуровневый вызов",
    "put": "client._request_handler.request('PUT', endpoint)  # низкоуровневый вызов",
    "patch": "client._request_handler.request('PATCH', endpoint)  # низкоуровневый вызов",
    "delete": "client._request_handler.request('DELETE', endpoint)  # низкоуровневый вызов",
    "create": "ITDClient(refresh_token=...)  # ClientInitResult убран в 1.x",
    "get_me": "client.users.me()",
    "get_user": "client.users.get()",
    "update_profile": "client.users.update_profile()",
    "follow_user": "client.users.follow()",
    "unfollow_user": "client.users.unfollow()",
    "get_followers": "client.users.get_followers()",
    "get_following": "client.users.get_following()",
    # posts
    "get_posts": "client.posts.list()",
    "get_post": "client.posts.get()",
    "create_post": "client.posts.create()",
    "update_post": "client.posts.update()",
    "delete_post": "client.posts.delete()",
    "like_post": "client.posts.like()",
    "unlike_post": "client.posts.unlike()",
    "repost_post": "client.posts.repost()",
    "get_user_posts": "client.posts.get_user_posts()",
    "vote": "client.posts.vote()",
    # comments
    "create_comment": "client.comments.create()",
    "reply_to_comment": "client.comments.reply()",
    "delete_comment": "client.comments.delete()",
    "like_comment": "client.comments.like()",
    "unlike_comment": "client.comments.unlike()",
    "get_comments": "client.comments.list()",
    "get_replies": "прямого аналога нет в 1.x  # отдельный list replies сейчас не реализован",
    # notifications
    "get_notifications": "client.notifications.list()",
    "mark_notification_read": "client.notifications.mark_read()",
    "mark_all_notification_read": "client.notifications.mark_all_read()",
    # files
    "upload_file": "client.files.upload()",
    # discovery / search
    "get_top_clans": "client.discovery.get_top_clans()",
    "who_to_follow": "client.discovery.who_to_follow()",
    "search_hashtags": "client.discovery.search_hashtags()",
    "search": "client.search.all()  # либо client.discovery.search()",
    "get_trending_hashtags": "client.discovery.get_trending_hashtags()",
    # pins
    "get_pins": "client.pins.get()",
    "set_pin": "client.pins.set()",
    "remove_pin": "client.pins.remove()",
    # settings
    "update_notification_settings": "client.users.update_notification_settings()",
    "update_privacy": "client.users.update_privacy()",
}


def get_suggestion(name: str) -> str:
    if name in SUGGESTIONS:
        return SUGGESTIONS[name]

    matches = difflib.get_close_matches(name, SUGGESTIONS.keys(), n=1)
    if matches:
        return SUGGESTIONS[matches[0]]

    return "см. документацию"
