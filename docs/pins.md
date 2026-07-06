# ITDpy
## Pins
Модуль `pins` позволяет:
-  получать пины
-  удалять пины
- ставить пины

# Получить текущие пины
```python
client.pins.get()
```
Возвращает модель `Pins`  [подробнее](models/pins.md)

### Пример:
```python
pins  =  client.pins.get()  
  
print("Активный пин:", pins.active_pin)  
  
print("\nВсе пины:")  
for  pin  in  pins.pins:  
  print("Slug:", pin.slug)  
  print("Название:", pin.name)  
  print("Описание:", pin.description)  
  print("Получен:", pin.granted_at)  
  print("-"  *  30)
```

# Ставить пины

```python 
client.pins.set(slug="kirill67_202602_infected")
```

# Удалять пины

```python 
client.pins.remove()
```

← [Назад к документации](index.md)
