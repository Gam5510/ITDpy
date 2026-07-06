# Config

`Config` управляет сетевыми настройками клиента, ретраями и таймаутами.

SDK использует **фиксированную и безопасную конфигурацию User-Agent**, которая не может быть изменена пользователем.

---

## Базовый пример

```python
from itdpy import Config, ITDClient

config = Config(
    timeout=30,
    upload_timeout=180,
    max_retries=5,
    backoff_factor=2.0,
    service="my_app"
)

client = ITDClient(
    refresh_token="YOUR_REFRESH_TOKEN",
    config=config,
)
```

---

## Все поля Config

```python
from itdpy import Config

config = Config(
    base_url="https://xn--d1ah4a.com",
    timeout=20,
    upload_timeout=120,
    max_retries=3,
    backoff_factor=1.5,
    sdk_version="1.0.5",
    service=None,
)
```

---

## Описание полей

### `base_url`

Базовый адрес API.

По умолчанию:

```python
"https://xn--d1ah4a.com"
```

Обычно менять не требуется.

---

### `timeout`

Таймаут обычных запросов (сек).

По умолчанию:

```python
20
```

---

### `upload_timeout`

Таймаут загрузки файлов (сек).

По умолчанию:

```python
120
```

---

### `max_retries`

Количество автоматических повторов при временных ошибках (`500`, `502`, `503`, `504`).

По умолчанию:

```python
3
```

---

### `backoff_factor`

Коэффициент задержки между повторами.

По умолчанию:

```python
1.5
```

---

### `sdk_version`

Версия SDK (используется в User-Agent).

Обычно не задаётся вручную.

---

### `service`

Имя вашего сервиса или приложения.

Пример:

```python
Config(service="my_app")
```

Используется для идентификации клиента в User-Agent.

---

## 🧠 User-Agent

SDK использует фиксированный формат:

```
itdpy/{version} (platform=python; type=sdk; service={service})
```

### Важно:

* User-Agent **не может быть изменён**
* SDK **не имитирует браузеры**
* SDK **не использует данные пользователя (user_id)**
* формат одинаков для всех клиентов

Это сделано для:

* прозрачности
* безопасности
* соответствия правилам платформы

---

## Как работает авторизация

SDK использует:

```python
refresh_token
```

### Важно:

* `refresh_token` используется для получения `access_token`
* `access_token` обновляется автоматически
* пользователю не нужно управлять токенами вручную

Альтернативно можно передать `email` и `password` вместо `refresh_token` —
SDK получит его автоматически через браузерный вход (см.
[Вход по email и паролю](quickstart.md#вход-по-email-и-паролю)) и сохранит
локально для последующих запусков.

---

## Пример без конфигурации

```python
from itdpy import ITDClient

client = ITDClient(
    refresh_token="YOUR_REFRESH_TOKEN"
)
```

---

## Ограничения

SDK не предназначена для:

* массовой автоматизации
* спама
* обхода ограничений
* имитации клиентов

---

## Рекомендации

* используйте `service` для идентификации приложения
* соблюдайте rate limits платформы
* обрабатывайте ошибки API
