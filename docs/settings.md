# ITDpy

## Settings

Модуль `settings` позволяет управлять:

-   настройками приватности профиля
-   настройками уведомлений

## Обновить настройки приватности
```python
client.users.update_privacy(  
  is_private=True,  
  wall_access="followers",  
  likes_visibility="mutual"  
)
```
### Параметры

Все параметры необязательны, но должен быть передан хотя бы один:

-   `is_private`    
-   `wall_access`    
-   `likes_visibility`    
-   `show_last_seen`
    
Если параметры не переданы — вызывается `ValueError`.

### Возвращает
Модель `PrivacySettings` [подробнее](models/settings.md)

## Пример
```python
privacy  =  client.users.update_privacy(  
  wall_access="mutual",  
  show_last_seen=False  
)  
  
print("Приватный профиль:", privacy.is_private)  
print("Стена:", privacy.wall_access)  
print("Лайки:", privacy.likes_visibility)  
print("Last seen:", privacy.show_last_seen)
```

## Обновить настройки уведомлений

```python
client.users.update_notification_settings(  
	comments=True,  
	mentions=True,  
	sound=False  
)
```
### Возвращает
Модель `PrivacySettings` [подробнее](models/settings.md)

## Особенности
-   Обновляются только переданные параметры.

## Пример
```python
updated = client.users.update_notification_settings(
    likes=False,
    sound=False,
    mentions=True
)

print("Обновлено!")
print("Лайки:", updated.likes)
print("Звук:", updated.sound)
print("Упоминания:", updated.mentions)
```

← [Назад к документации](index.md)