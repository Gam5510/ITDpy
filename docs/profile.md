# ITDpy

## Profile

Модуль `profile` позволяет обновлять данные текущего пользователя.

----------

## Обновить профиль
```python
client.users.update_profile(  
  display_name="Фазлиддин",  
  bio="Python developer",  
  banner_id="ссылка_на_загруженный_файл"  
)
```
### Параметры:

-   `display_name` — отображаемое имя пользователя
-   `username` — новый username
-   `bio` — описание профиля
-   `banner_id` — [ссылка загруженного файла](upload.md) 
    
Все параметры являются необязательными, но должен быть передан хотя бы один.

----------

### Возвращает

Модель `Me` [подробнее](models/users.md)

----------

## Пример использования
```python
me  =  client.users.update_profile(  
  display_name="Фазлиддин",  
  bio="Разрабатываю ITDpy"
  banner_id = "https://943701f000610900cbe86b72234e451d.bckt.ru/images/db3fb2d8-70ad-4761-a073-0b39288d1205.gif"  
)  
  
print("ID:", me.id)  
print("Username:", me.username)  
print("Display name:", me.display_name)  
print("Bio:", me.bio)  
print("Banner:", me.banner)
```

← [Назад к документации](index.md)