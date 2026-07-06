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
from itdpy import ITDClient

client = ITDClient(refresh_token="YOUR_REFRESH_TOKEN")

me = client.users.get_me()
print(me.id)
print(me.username)
```

## 🔐 Вход по email и паролю

Вместо `refresh_token` можно передать `email` и `password` — SDK сам пройдёт
через браузер капчу Cloudflare Turnstile, авторизуется и получит `refresh_token`
(см. [Turnstile Interceptor](#-turnstile-interceptor) ниже).

```python
from itdpy import ITDClient

client = ITDClient(email="user@example.com", password="my-password")

me = client.users.get_me()
print(me.username)
```

SDK **не сохраняет** email/password/refresh_token на диск — вход выполняется
заново через браузер при каждой инициализации клиента и при истечении сессии.
Если вам нужно переиспользовать `refresh_token` между запусками, сохраняйте
его самостоятельно (например, через `on_refresh_token_update`) в защищённом
хранилище на ваше усмотрение:

```python
client = ITDClient(
    email="user@example.com",
    password="my-password",
    on_refresh_token_update=lambda token: print("Новый refresh_token:", token),
)
```

### 🔁 Автообновление сессии (без повторных логинов)

Держите `ITDClient` как один долгоживущий объект (не создавайте новый на
каждый запрос) — тогда браузер и логин по email/password запускаются один
раз. По умолчанию клиент сам раз в 4.5 минуты (`auto_refresh_interval=270`
сек) обновляет `access_token` по имеющемуся `refresh_token` в фоновом потоке
— без повторного открытия браузера и без повторного входа в аккаунт:

```python
client = ITDClient(email="user@example.com", password="my-password")
# клиент можно использовать сколько угодно — сессия обновляется сама
```

Изменить интервал или отключить автообновление:

```python
client = ITDClient(
    email="user@example.com",
    password="my-password",
    auto_refresh_interval=200,  # секунд
)

# либо полностью выключить и обновлять вручную
client = ITDClient(
    email="user@example.com",
    password="my-password",
    auto_refresh_interval=None,
)
```

Фоновый поток останавливается автоматически при `client.close()`.

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

## 🛡 Turnstile Interceptor

Этот скрипт предназначен для перехвата токена авторизации Cloudflare Turnstile и отправки самостоятельного запроса к API. Скрипт является кроссплатформенным:
На Windows и macOS он работает в обычном оконном режиме (откроется браузер).
На Linux-серверах (без монитора) скрипт автоматически создает виртуальный экран с помощью Xvfb, чтобы обойти блокировки Cloudflare, которые жестко пресекают классический headless режим.

### 🌐 Можно ли использовать обычный установленный Chrome?

Да. **DrissionPage не скачивает и не устанавливает свой браузер** — он подключается к уже установленному в системе Google Chrome (или Microsoft Edge/Chromium) через протокол CDP и управляет им напрямую. Отдельно устанавливать Chromium не нужно, если Chrome уже стоит на компьютере.

- Обычно путь к браузеру находится **автоматически** (Windows/macOS/Linux) — ничего указывать не требуется.
- Если автоопределение не сработало (нестандартная папка установки, portable-версия, несколько браузеров в системе), укажите путь к `chrome.exe` явно:

```python
from itdpy import ITDClient

client = ITDClient(
    email="user@example.com",
    password="my-password",
    browser_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
)
```

или напрямую при использовании низкоуровневой функции:

```python
from itdpy.auth import login_with_password

refresh_token = login_with_password(
    "user@example.com",
    "my-password",
    browser_path="/usr/bin/google-chrome",
)
```

### 📥 Установка Chromium/Chrome, если браузера в системе нет

**Windows / macOS** — просто установите обычный Google Chrome с официального сайта: https://www.google.com/chrome/. Никаких дополнительных шагов не требуется — DrissionPage найдёт его сам.
**Linux (сервер без GUI)** — установите Chromium или Google Chrome из репозитория:

```bash
# Вариант 1: Chromium из репозитория (проще всего)
sudo apt-get update
sudo apt-get install chromium-browser

# Вариант 2: официальный Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt-get install ./google-chrome-stable_current_amd64.deb
```

После установки браузер будет найден автоматически. Если он лежит в нестандартном месте, узнайте путь командой `which chromium-browser` (или `which google-chrome`) и передайте его через `browser_path`, как показано выше.
Xvfb (виртуальный дисплей, см. ниже) — это отдельная от самого браузера зависимость, нужна на Linux в любом случае, т.к. Cloudflare блокирует классический `--headless` режим.

### 💻 Установка на локальный ПК (Windows / macOS)

Все необходимые библиотеки (`requests`, `DrissionPage` и т.д.) уже входят в
зависимости `itdpy` по умолчанию — достаточно `pip install itdpy`, отдельно
ничего доустанавливать не нужно. Нужен только установленный Google Chrome
(см. раздел выше).

### 🐧 Установка на сервер (Ubuntu / Debian / Linux)

Так как на сервере нет графической оболочки (GUI), мы должны эмулировать монитор. Без этого Chromium откажется запускаться без флага headless, а с флагом headless Cloudflare заблокирует скрипт.

**Шаг 1. Установка системных зависимостей**

Установите виртуальный фреймбуфер Xvfb:

```bash
sudo apt-get update
sudo apt-get install xvfb
```

(Опционально) Если на чистом сервере не установлены нужные библиотеки для работы самого браузера Chromium (шрифты, графические пакеты), вы можете установить их с помощью Playwright:

```bash
pip install playwright
playwright install-deps chromium
```

**Шаг 2. Установка Python-библиотек**

```bash
pip install itdpy
```

`DrissionPage` и `pyvirtualdisplay` (обёртка для виртуального дисплея на
Linux) уже входят в зависимости `itdpy` по умолчанию — устанавливать их
отдельно не нужно.

Скрипт автоматически распознает Linux, поднимет невидимый дисплей, запустит браузер "с головой" внутри этого дисплея, пройдет все проверки, заберет токен и завершит работу.

### 💡 Как это работает?

Скрипт внедряет JavaScript на страницу вашего сайта.
Подменяет глобальную функцию fetch.
Когда React собирается отправить запрос sign-in, наш шпион читает turnstileToken из тела запроса.
Шпион блокирует оригинальный запрос браузера (замораживает его).
Скрипт закрывает браузер и отправляет чистый запрос к API через библиотеку requests, подставляя нужные куки и токен.

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

## Поддежка проекта 
Вы можете поддержать проект с помощью перевода по TON кошельку в сети TON 
UQBVKStaBRLERdjJ_dnzRfREzqmyzkQn14uDE-DleRXJBqqH
