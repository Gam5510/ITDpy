# Files API

## Upload файла

```python
file = client.files.upload("test.jpg")

print(file.id)
print(file.url)
print(file.filename)
print(file.mime_type)
```

## Получить файл

```python
file = client.files.get("FILE_ID")
print(file.to_json())
```

## Удалить файл

```python
client.files.delete("FILE_ID")
```
