# Обзор API

В `itdpy` основные группы API доступны через свойства клиента:

```python
client.posts
client.comments
client.notifications
client.users
client.files
client.search
client.discovery
client.pins
```

## Posts

- `list()`
- `list_all()`
- `get()`
- `create()`
- `post_to_wall()`
- `update()`
- `delete()`
- `like()`
- `unlike()`
- `repost()`
- `get_user_posts()`
- `get_all_user_posts()`
- `vote()`
- `view()`
- `view_many()`

## Comments

- `list()`
- `list_all()`
- `create()`
- `reply()`
- `update()`
- `like()`
- `unlike()`
- `delete()`

## Notifications

- `list()`
- `list_all()`
- `mark_read()`
- `mark_all_read()`
- `stream()`

## Users

- `me()`
- `get()`
- `follow()`
- `unfollow()`
- `get_followers()`
- `get_following()`
- `follow_status()`
- `update_profile()`
- `update_privacy()`
- `update_notification_settings()`
- `block()`
- `unblock()`

## Search

- `all()`
- `users()`
- `hashtags()`

## Discovery

- `portal()`
- `get_top_clans()`
- `who_to_follow()`
- `search()`
- `search_hashtags()`
- `get_trending_hashtags()`

## Files

- `upload()`
- `get()`
- `delete()`
