# ITDpy

Python SDK для социальной сети ITD.
Упрощает работу с SDK API и позволяет быстро писать ботов и автоматизации.


## Установка pip
```bash
pip install itdpy
```

### Через git

```bash
git clone https://github.com/Gam5510/ITDpy
cd itdpy
pip install -r requirements.txt
pip install -e .
```

## Быстрый старт

> Blockquote ![Получение токена](https://i.ibb.co/DH1m8GL7/Assistant.png)
Как получить токен

```python
from  itdpy.client  import  ITDClient
from  itdpy.auth  import  AuthManager
from  itdpy.api  import  get_me

client  =  ITDClient(refresh_token="Ваш refresh token")

auth  =  AuthManager(client)
auth.refresh_access_token()
  
me  =  get_me(client)
print(me.id)
print(me.username)
```

### Скрипт на обновление имени

```python
from  itdpy.client  import  ITDClient
from  itdpy.auth  import  AuthManager
from  itdpy.api  import  update_profile
from  datetime  import  datetime
import  time

client = ITDClient(refresh_token="Ваш_токен")
auth = AuthManager(client)

auth.refresh_access_token()

while  True:
	update_profile(client,  display_name=f"Фазлиддин |{datetime.now().strftime('%m.%d %H:%M:%S')}|")
	time.sleep(1)
```

### Скрипт на обновление баннера 
```python
from  itdpy.client  import  ITDClient
from  itdpy.auth  import  AuthManager
from  itdpy.api  import  update_profile, upload_file
from  datetime  import  datetime
import  time

client  =  ITDClient(refresh_token="Ваш_токен")
auth  =  AuthManager(client)
auth.refresh_access_token()

file  =  upload_file(client,  "matrix-rain-effect-animation-photoshop-editor.gif")
print(file.id)
update  =  update_profile(client,  banner_id=file.id)
print(update.banner)
```

# Костомные запросы  

## ✅ Базовый пример кастомного GET
```python
response = client.get("/api/users/me")
data = response.json() 
print(data)
```
### Можно добавить любой эндпоинт
----------

## ✅ POST с JSON
```python
response = client.post( 
		"/api/posts",
    json={ "content": "Привет из кастомного запроса" }
) 
print(response.status_code) 
print(response.json())
```
----------

## ✅ PUT / PATCH
```python
response = client.patch( "/api/profile",
    json={ "displayName": "Фазлиддин 😎" }
)
```
----------

## ✅ DELETE
```python
client.delete("/api/posts/POST_ID") 
```
----------

## ✅ Передача query-параметров
```python
response = client.get( "/api/posts",
    params={ "limit": 50, "sort": "popular" }
)
```

## Планы

- Асинхронная версия библиотеки (`aioitd`)
- Улучшенная обработка и форматирование ошибок
- Логирование (через `logging`)
- Расширение объектной модели (Post, Comment, User и др.)
- Дополнительные API-эндпоинты по мере появления
- Улучшение документации и примеров


## Прочее

Проект активно развивается.
Если у вас есть идеи или предложения — создавайте issue или pull request.
