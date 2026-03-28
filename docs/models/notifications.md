# ITDpy

## Модель Notification

### Пример ответа Notification
```json
{
      "id": "08007db7-b4da-4f45-a365-2ace3a57987f",
      "type": "follow",
      "targetType": null,
      "targetId": null,
      "preview": null,
      "readAt": "2026-02-16T10:51:44.288Z",
      "createdAt": "2026-02-15T16:01:07.511Z",
      "actor": {
        "id": "330dea20-bb7c-4c96-ad09-97150f1ad5f6",
        "displayName": "TM",
        "username": "FIRST_TM",
        "avatar": "™"
      },
      "read": true
}
```

|Поле|Тип|Описание|
|--|--|--|
|id|str|ID уведомления|
|type|str|Тип события (`like`, `comment`, `reply`, `repost`, `follow`, `wall_post` и др.)|
|target_type|str|Откуда уведомление, например `post` и др.|
|target_id|str|ID к источнику из `target_type`|
|preview|str|Краткий текст уведомление|
|read|bool|Прочитано ли уведомление|
|read_at|str|Время прочтение|
|created_at|str|Дата создание уведомление |
|actor|[Actor](actor.md)|Модель Actor|

## Пример использование:
```python
notifications  =  client.get_notifications(limit=50)

print("Всего уведомлений:",  len(notifications))
print("-"  *  50)
  
for  n  in  notifications:
	
	print("ID:",  n.id)
	print("Тип:",  n.type)
	print("Прочитано:",  n.read)
	print("Создано:",  n.created_at)
	
	if  n.target_type:
		print("Источник:",  n.target_type)
		print("ID источника:",  n.target_id)  
		
	if  n.preview:
		print("Текст:",  n.preview)

	if  n.read_at:
		print("Прочитано в:",  n.read_at)
  
	if  n.actor:
		print("Actor ID:",  n.actor.id)
		print("Actor username:",  n.actor.username)
		print("Actor display:",  n.actor.display_name)
		print("Actor avatar:",  n.actor.avatar)

	print("="  *  50)
```

← [Назад к документации](../index.md)
