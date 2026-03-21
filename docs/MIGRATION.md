# MIGRATION GUIDE (0.x → 1.0)

В мажорной версии `1.0` архитектура **ITDpy** была значительно улучшена, чтобы предоставить Pythonic интерфейс, строгую типизацию и более чистый код. В связи с этим, некоторые старые подходы перестали работать.

## 1. Замена плоских методов на пространства имен (Namespace API)

Ранее у `ITDClient` методы были свалены в кучу. Теперь они строго разделены по логическим группам.

### Было (OLD)
```python
client.get_posts()
client.create_post(...)
client.get_user("gam5510")
client.follow_user(...)
```

### Стало (NEW)
```python
client.posts.list()
client.posts.create(...)
client.users.get("gam5510")
client.users.follow(...)
```

## 2. Гибкие Модели (Pydantic) вместо обычных словарей

Вся библиотека переведна на гибкие Pydantic v2 модели, которые поддерживают как строгие атрибуты, так и обращение как к словарю (`dict`).

### Стало (NEW)
Возвращаются объекты Pydantic: `Post`, `User`, `PostsList`, `UsersList`. Поля в объектах пишутся через `snake_case`, но также можно обращаться к ним по оригинальным camelCase ключам!

```python
me = client.users.me()

# Как атрибут
print(me.id) 
print(me.display_name)

# Как к словарю
print(me["displayName"])

# Преобразования
print(me.to_dict())
print(me.to_json())
```

## 3. Использование Enums вместо строк

Вместо магических строк теперь используются перечисления.

### Было (OLD)
```python
client.get_posts(tab="newest")
```

### Стало (NEW)
```python
from itdpy.enums import PostsTab

client.posts.list(tab=PostsTab.NEWEST)
```

## 4. Пагинация

Модели типа `PostsList` и `UsersList` теперь хранят данные о пагинации.
- Вы можете обратиться к массиву элементов через атрибут `items`
- Свойства пагинации: `cursor` и `has_more`

## 5. Streaming API

Стриминг вынесен в `client.notifications.stream()`. 

Метод `client.keep_online()` сохранен, но теперь он более стабильно переводит стрим в фоновый поток (если `background=True`).
