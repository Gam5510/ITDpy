# ITDpy

## Модели Pin, Pins

Пин это награда, отображающаяся в профиле пользователя.  
Каждый пин содержит метаданные и дату получения.

----------
# Модель Pin
## Пример ответа Pin
```json
{  
 "slug": "kirill67_202602_infected",  
 "name": "Переболел вирусом Кирилл-67",  
 "description": "Вирус (Февраль, 2026г)",  
 "grantedAt": "2026-02-07T10:22:08.454Z"  
}
```
------
### Поля объекта Pin
| Поле | Тип | Описание |
|------|-----|----------|
| slug | str | ID пина |
| name| str | Название пина|
| description| str | Описание пина|
| granted_at| str | Дата получения|

------

# Модель Pins
## Пример ответа Pins
```json
{  
 "data": {  
 "pins": [  
 {  
 "slug": "kirill67_202602_infected",  
 "name": "Переболел вирусом Кирилл-67",  
 "description": "Вирус (Февраль, 2026г)",  
 "grantedAt": "2026-02-07T10:22:08.454Z"  
 }  
 ],  
 "activePin": "kirill67_202602_infected"  
 }  
}
```
------
### Поля объекта Pins
| Поле | Тип | Описание |
|------|-----|----------|
| pins| list[Pin]| Список доступных пользователю пинов |
| active_pin| str | Slug текущего установленного пина|

# Пример использования
```python
pins  =  client.get_pins()  
  
print("Активный пин:", pins.active_pin)  
  
print("\nВсе пины:")  
for  pin  in  pins.pins:  
  print("Slug:", pin.slug)  
  print("Название:", pin.name)  
  print("Описание:", pin.description)  
  print("Получен:", pin.granted_at)  
  print("-"  *  30)
```

← [Назад к документации](../index.md)