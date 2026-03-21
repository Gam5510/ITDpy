# Модели User и UsersList

## User

```python
user = client.users.get("username")

print(user.id)
print(user.username)
print(user.display_name)
print(user.avatar)
print(user.to_json())
```

## UserLite

Используется во вложенных сущностях:

- `post.author`
- `post.wall_recipient`
- `comment.author`
- `notification.actor`

SDK автоматически понимает разные варианты ключей сервера:

- `avatar`
- `isVerified`, `verified`, `verifieed`
- `username` и `userrname`

## UsersList

```python
followers = client.users.get_followers("USER_ID")

print(len(followers))
print(followers.page)
print(followers.total)
print(followers.has_more)
print(followers.to_json())
```
