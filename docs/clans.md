# ITDpy

## Clans

Модуль `clans` позволяет:

-   получать топ кланов

## Получить топ кланов
```python
client.discovery.get_top_clans()
```

### Пример ответа
```json
{
    "clans": [
        {
            "avatar": "🦎",
            "memberCount": 20693
        },
        {
            "avatar": "🤡",
            "memberCount": 9983
        },
        {
            "avatar": "👀",
            "memberCount": 7107
        },
        {
            "avatar": "💀",
            "memberCount": 6091
        },
        {
            "avatar": "😎",
            "memberCount": 5319
        },
        {
            "avatar": "👾",
            "memberCount": 5285
        },
        {
            "avatar": "💩",
            "memberCount": 4600
        },
        {
            "avatar": "😈",
            "memberCount": 4194
        },
        {
            "avatar": "😁",
            "memberCount": 4182
        },
        {
            "avatar": "😀",
            "memberCount": 3806
        }
    ]
}
```
 
### Пример использование 
```python
top  =  client.discovery.get_top_clans()

print("Топ кланов:")
print("-"  *  40)

for  index,  clan  in  enumerate(top.get("clans",  []),  start=1):
	print(f"{index}. {clan['avatar']} — {clan['memberCount']} участников")
```

← [Назад к документации](index.md)