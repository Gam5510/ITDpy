# ITDpy

<p align="center">
  <img src="https://i.postimg.cc/gJ9z8RDk/ITDpy-(1)-pixian-ai.png" width="700">
</p>

<p align="center">
  <img src="https://img.shields.io/pypi/v/itdpy?nocache=1" alt="PyPI version">
  <img src="https://static.pepy.tech/badge/itdpy?nocache=1" alt="Downloads">
  <img src="https://img.shields.io/github/license/Gam5510/ITDpy" alt="License">
  <a href="https://gam5510.github.io/ITDpy/">
    <img src="https://img.shields.io/badge/docs-online-blue" alt="Docs">
  </a>
</p>

Python SDK для интеграции с платформой ИТД.com.

> SDK предназначен для клиентских приложений, интеграций и сервисов.
> Проект ориентирован на безопасное, прозрачное и корректное взаимодействие с платформой.

## Принципы безопасности

ITDpy разработан с акцентом на доверие и соблюдение правил платформы:

прозрачная идентификация клиента через User-Agent
отсутствие маскировки под браузер
отсутствие обхода ограничений платформы
соблюдение rate limits и правил API

### SDK не поддерживает:

- спам
- массовую автоматизацию
- накрутку
- любые формы злоупотребления API

## User-Agent

ITDpy использует фиксированный и прозрачный формат User-Agent:

itdpy/{version} (platform=python; type=sdk; service={service})

- User-Agent не может быть изменён пользователем
- SDK не имитирует браузеры или мобильные клиенты
- это позволяет платформе корректно идентифицировать источник трафика

## 📦 Установка
```bash
pip install itdpy
```

## 🚀 Быстрый старт
```python
from itdpy import Client

client = Client(refresh_token="YOUR_REFRESH_TOKEN")

me = client.users.get_me()
print(me.id)
print(me.username)
```

## ⚙️ Конфигурация

```python
from itdpy import Client, Config

config = Config(
    service="my_application"
)

client = Client(config=config, refresh_token="TOKEN")
```

Доступные параметры:

- `service` — имя вашего сервиса (используется в User-Agent)
- `timeout` — таймаут запросов
- `max_retries` — количество повторов

## 📚 Документация

[https://gam5510.github.io/ITDpy/](https://gam5510.github.io/ITDpy/)

## ⚠️ Ограничения

SDK не предназначена для:

- массовых автоматизированных действий
- обхода ограничений платформы
- использования в целях, нарушающих правила

## 🤝 Сотрудничество

Проект открыт к взаимодействию с платформой ИТД.com и ориентирован на официальную интеграцию.

Если вы представляете платформу или хотите обсудить сотрудничество, то свяжитесь через GitHub или Telegram.

## Обратная связь

Telegram: [@gam5510](https://t.me/gam5510)
GitHub Issues: [https://github.com/Gam5510/ITDpy](https://github.com/Gam5510/ITDpy)