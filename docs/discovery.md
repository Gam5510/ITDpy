# Discovery API

## Portal

```python
portal = client.discovery.portal()
print(portal.to_dict())
```

Пример ответа:

```python
{
    "active": True,
    "title": "PixelBattle",
    "url": "https://pixel.xn--d1ah4a.com/"
}
```

## Топ кланы

```python
top_clans = client.discovery.get_top_clans()
print(top_clans.to_json())
```

## Кого читать

```python
suggestions = client.discovery.who_to_follow()
print(suggestions.to_json())
```

## Поиск

```python
result = client.discovery.search("python")
print(result.users.to_json())
```

## Посты по хэштегу

```python
posts = client.discovery.search_hashtags("python", limit=20)
print(posts.to_json())
```

## Trending hashtags

```python
trending = client.discovery.get_trending_hashtags(limit=10)
print(trending.to_json())
```
