# Posts API

## Получить ленту

```python
from itdpy import PostsTab

posts = client.posts.list(limit=20, tab=PostsTab.POPULAR)
print(posts.to_json())
```

## Получить всю ленту

`list_all()` забирает посты батчами по `50`.

```python
all_posts = client.posts.list_all(limit=120)
print(len(all_posts))
```

## Получить пост

```python
post = client.posts.get("POST_ID")
print(post.to_json())
```

## Создать пост

```python
post = client.posts.create(content="Привет")
```

## Markdown / HTML

```python
client.posts.create(content="**Жирный**", parse_md=True)
client.posts.create(content="<b>Жирный</b>", parse_html=True)
```

## Пост на чужую стену

По `username`:

```python
post = client.posts.post_to_wall(
    username="username",
    content="Привет на стену",
)
```

По `user_id`:

```python
post = client.posts.post_to_wall(
    user_id="USER_ID",
    content="Привет на стену по id",
)
```

## Обновить пост

```python
updated = client.posts.update("POST_ID", content="Новый текст")
print(updated.updated_at)
```

`client.posts.update(...)` возвращает `PostUpdate`.

## Лайки и репосты

```python
likes = client.posts.like("POST_ID")
client.posts.unlike("POST_ID")
repost = client.posts.repost("POST_ID", content="Мой репост")
```

## Посты пользователя

```python
from itdpy import UserPostSorting

posts = client.posts.get_user_posts("username", sort=UserPostSorting.NEW)
all_posts = client.posts.get_all_user_posts("username", limit=100)
```

## Poll

```python
from itdpy.models import PollBuilder

post = client.posts.create(
    content="Голосуем",
    poll=PollBuilder("Как подавать котлеты?")
        .add("С пюрешкой")
        .add("Без пюрешки"),
)
```

## Голосование

```python
poll = client.posts.vote(post_id="POST_ID", option_ids="OPTION_ID")
print(poll.to_json())
```

## Просмотр поста

```python
view = client.posts.view("POST_ID")
views = client.posts.view_many(["POST_ID_1", "POST_ID_2"])
```
