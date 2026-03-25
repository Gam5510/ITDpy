# Config

`Config` управляет сетевыми настройками клиента, ретраями, таймаутами и поведением `User-Agent`.

## Базовый пример

```python
from itdpy import Config, ITDClient

config = Config(
    timeout=30,
    upload_timeout=180,
    max_retries=5,
    backoff_factor=2.0,
)

client = ITDClient(
    refresh_token="YOUR_REFRESH_TOKEN",
    config=config,
)
```

## Все поля Config

```python
from itdpy import Config

config = Config(
    base_url="https://xn--d1ah4a.com",
    timeout=20,
    upload_timeout=120,
    max_retries=3,
    backoff_factor=1.5,
    sdk_version="1.0.2",
    service=None,
    initial_user_agent=(
        "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/146.0.0.0 Mobile Safari/537.36"
    ),
    custom_user_agent=None,
    user_agent_template="itdpy/{sdk_version} ({parts})",
    use_user_data_in_user_agent=False,
)
```

## Описание полей

### `base_url`

Базовый адрес API.

По умолчанию:

```python
"https://xn--d1ah4a.com"
```

Обычно менять не нужно. Поле пригодится только если у тебя есть тестовый стенд, прокси или отдельный gateway.

### `timeout`

Таймаут обычных запросов в секундах.

По умолчанию:

```python
20
```

Используется для стандартных API-вызовов, где нет загрузки файлов.

### `upload_timeout`

Таймаут загрузки файлов в секундах.

По умолчанию:

```python
120
```

Нужен отдельно, потому что upload-запросы могут идти заметно дольше обычных.

### `max_retries`

Количество автоматических повторов для временных сетевых ошибок и ответов сервера `500`, `502`, `503`, `504`.

По умолчанию:

```python
3
```

Если API иногда отвечает нестабильно, это поле помогает пережить кратковременные сбои без ручной логики повтора.

### `backoff_factor`

Коэффициент задержки между повторами.

По умолчанию:

```python
1.5
```

Чем больше значение, тем осторожнее библиотека ведёт себя при повторных попытках.

### `sdk_version`

Версия SDK, которая может использоваться в шаблоне `User-Agent`.

По умолчанию:

```python
"1.0.2"
```

Обычно вручную не задаётся.

### `service`

Имя твоего приложения или сервиса.

Пример:

```python
Config(service="my_app")
```

Это поле используется только если включён режим `use_user_data_in_user_agent=True` или если ты сам используешь его в `user_agent_template`.

### `initial_user_agent`

Стартовый `User-Agent`, который библиотека использует по умолчанию.

По умолчанию:

```python
"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36"
```

Это не декоративная настройка, а вынужденная мера совместимости.

Причина:

- refresh-запрос к API может не работать с дефолтным `python-requests/...`
- сервер может воспринимать такой запрос как бот
- без браузерного стартового профиля аутентификация может ломаться

ITDpy использует этот стартовый `User-Agent`, чтобы библиотека работала стабильно.

Проект не поддерживает спам, абьюз API и вредоносную автоматизацию. Эта настройка нужна только для совместимости клиентских и сервисных сценариев.

### `custom_user_agent`

Полностью переопределяет `User-Agent`.

Пример:

```python
Config(custom_user_agent="my-app/2.0")
```

Если поле задано, библиотека будет использовать именно его вместо `initial_user_agent` и вместо шаблонного SDK `User-Agent`.

Это самый прямой способ задать собственный `User-Agent`.

### `user_agent_template`

Шаблон `User-Agent`, который используется после авторизации, если включён `use_user_data_in_user_agent=True`.

По умолчанию:

```python
"itdpy/{sdk_version} ({parts})"
```

Доступные плейсхолдеры:

- `{sdk_version}`
- `{parts}`
- `{user_id}`
- `{service}`

Пример:

```python
Config(
    use_user_data_in_user_agent=True,
    user_agent_template="itdpy/{sdk_version} (uid={user_id}; {parts}; service={service})",
)
```

### `use_user_data_in_user_agent`

Флаг, который включает переключение на `User-Agent` с данными пользователя после успешной авторизации.

По умолчанию:

```python
False
```

Когда флаг выключен:

- библиотека продолжает использовать `initial_user_agent`
- это самый безопасный режим совместимости

Когда флаг включен:

- после `users/me` библиотека собирает новый `User-Agent`
- в него могут попасть `userid`, `platform=python` и `service`

Пример:

```python
from itdpy import Config, ITDClient

config = Config(
    service="my_app",
    use_user_data_in_user_agent=True,
)

client = ITDClient(
    refresh_token="YOUR_REFRESH_TOKEN",
    config=config,
)
```

## Как работает User-Agent в библиотеке

Логика такая:

1. При создании сессии библиотека ставит стартовый `User-Agent`.
2. Если задан `custom_user_agent`, используется он.
3. Если `custom_user_agent` не задан, используется `initial_user_agent`.
4. Если включён `use_user_data_in_user_agent=True`, после авторизации `User-Agent` обновляется по шаблону `user_agent_template`.

## Рекомендуемые сценарии

### Обычное использование

Ничего дополнительно настраивать не нужно:

```python
from itdpy import ITDClient

client = ITDClient(refresh_token="YOUR_REFRESH_TOKEN")
```

В этом режиме библиотека использует безопасный стартовый браузерный `User-Agent`.

### Свой User-Agent

```python
from itdpy import Config, ITDClient

config = Config(custom_user_agent="my-app/2.0")
client = ITDClient(refresh_token="YOUR_REFRESH_TOKEN", config=config)
```

### User-Agent с данными сервиса и пользователя

```python
from itdpy import Config, ITDClient

config = Config(
    service="my_app",
    use_user_data_in_user_agent=True,
)

client = ITDClient(refresh_token="YOUR_REFRESH_TOKEN", config=config)
```

## Что выбрать

- Если тебе нужна просто рабочая библиотека, используй настройки по умолчанию.
- Если у тебя свой сервис и нужен собственный идентификатор клиента, используй `custom_user_agent`.
- Если тебе нужен шаблонный SDK `User-Agent` с `userid/service`, включай `use_user_data_in_user_agent=True`.
