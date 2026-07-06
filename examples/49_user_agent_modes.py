"""
Пример использования двух режимов User-Agent в itdpy SDK.

Два режима работы:
1. "compat" (по умолчанию) - Browser-like User-Agent для совместимости
2. "safe" - Прозрачный SDK User-Agent
"""

from itdpy import Client, Config


# ============================================================================
# РЕЖИМ 1: "compat" (по умолчанию) - Совместимость с API
# ============================================================================

def example_compat_mode():
    """
    Compat режим использует browser-like User-Agent.
    Это текущее поведение SDK и рекомендуется оставлять по умолчанию.
    """
    config = Config(
        mode="compat",  # явно указываем (по умолчанию)
    )

    # User-Agent будет:
    # "Mozilla/5.0 (Linux; Android 11; SM-G991B)AppleWebKit/537.36 ..."
    print("Compat mode User-Agent:")
    print(config.get_user_agent())
    # => Mozilla/5.0 (Linux; Android 11; SM-G991B)AppleWebKit/537.36...


# ============================================================================
# РЕЖИМ 2: "safe" - Прозрачный SDK User-Agent
# ============================================================================

def example_safe_mode():
    """
    Safe режим использует прозрачный SDK User-Agent с форматом:
    "itdpy/{sdk_version} ({parts})"
    """
    config = Config(
        mode="safe",
    )

    # User-Agent будет:
    # "itdpy/1.0.2 (platform=python)"
    print("\nSafe mode User-Agent (базовый):")
    print(config.get_user_agent())
    # => itdpy/1.0.2 (platform=python)


def example_safe_mode_with_service():
    """
    Safe режим с указанием сервиса (приложения, которое использует SDK).
    """
    config = Config(
        mode="safe",
        service="my-bot",  # имя вашего приложения/бота
    )

    # User-Agent будет:
    # "itdpy/1.0.2 (platform=python; service=my-bot)"
    print("\nSafe mode User-Agent (с сервисом):")
    print(config.get_user_agent())
    # => itdpy/1.0.2 (platform=python; service=my-bot)


def example_safe_mode_with_user_data():
    """
    Safe режим с включением данных пользователя (user_id).
    Включается после авторизации через use_user_data_in_user_agent.
    """
    config = Config(
        mode="safe",
        service="my-analytics-bot",
        use_user_data_in_user_agent=True,
    )

    # До авторизации (user_id = None):
    # "itdpy/1.0.2 (initial; platform=python; service=my-analytics-bot)"
    print("\nSafe mode User-Agent (до авторизации):")
    print(config.get_user_agent())
    # => itdpy/1.0.2 (initial; platform=python; service=my-analytics-bot)

    # После авторизации (user_id доступен):
    user_id = "user_12345"
    print("\nSafe mode User-Agent (после авторизации):")
    print(config.get_user_agent(user_id=user_id))
    # => itdpy/1.0.2 (userid=user_12345; platform=python; service=my-analytics-bot)


# ============================================================================
# ПРИОРИТЕТ: custom_user_agent переопределяет всё
# ============================================================================

def example_custom_user_agent():
    """
    Если задан custom_user_agent, он всегда используется,
    независимо от режима и других настроек.
    """
    config = Config(
        mode="safe",  # даже если включен safe режим
        custom_user_agent="my-custom-app/2.0 (python)",
    )

    # User-Agent будет именно "my-custom-app/2.0 (python)", несмотря на mode="safe"
    print("\nCustom User-Agent (переопределяет режим):")
    print(config.get_user_agent())
    # => my-custom-app/2.0 (python)


# ============================================================================
# РЕАЛЬНЫЙ ПРИМЕР: Клиент в разных режимах
# ============================================================================

async def example_client_compat_mode():
    """
    Использование Client в режиме compat (по умолчанию).
    Подходит для большинства случаев и задней совместимости.
    """
    config = Config()  # mode="compat" по умолчанию

    async with Client(config=config, access_token="your_token") as client:
        # User-Agent автоматически выбирается из config
        me = await client.users.me()
        print(f"Current user: {me}")


async def example_client_safe_mode():
    """
    Использование Client в режиме safe для прозрачности.
    Рекомендуется для приложений, где важна отчетность о источнике трафика.
    """
    config = Config(
        mode="safe",
        service="my-awesome-bot",
        use_user_data_in_user_agent=True,
    )

    async with Client(config=config, access_token="your_token") as client:
        # После авторизации User-Agent будет содержать user_id
        me = await client.users.me()
        print(f"Current user: {me}")
        # На сервере увидят:
        # "itdpy/1.0.2 (userid=<user_id>; platform=python; service=my-awesome-bot)"


# ============================================================================
# ТАБЛИЦА ПРИОРИТЕТОВ
# ============================================================================

def show_priority_table():
    """
    Таблица приоритетов выбора User-Agent:

    Приоритет 1: custom_user_agent (если задан)
    Приоритет 2: mode == "safe" (используется SDK User-Agent)
    Приоритет 3: mode == "compat" (browser-like User-Agent)
    """
    examples = [
        ("custom_user_agent задан", Config(custom_user_agent="my-app/1.0")),
        ("mode='safe'", Config(mode="safe")),
        ("mode='compat' (default)", Config()),
    ]

    print("\n=== ТАБЛИЦА ПРИОРИТЕТОВ ===\n")
    for desc, config in examples:
        ua = config.get_user_agent(user_id="123")
        print(f"{desc:35} => {ua}")


# ============================================================================
# МИГРАЦИЯ С ТЕКУЩЕЙ ВЕРСИИ
# ============================================================================

def migration_guide():
    """
    Для существующих пользователей:
    
    ✅ Если ничего не менять - всё работает как раньше (режим compat по умолчанию)
    
    ✅ Если хотите включить safe режим:
       config = Config(mode="safe")
    
    ✅ Если хотите свой User-Agent:
       config = Config(custom_user_agent="my-app/1.0")
    
    ✅ Если использовали initial_user_agent для переопределения:
       # Старый способ (больше не работает):
       config.initial_user_agent = "my-custom"
       
       # Новый способ:
       # Либо используйте mode="compat" и default compatibility_user_agent
       # Либо используйте custom_user_agent
       config = Config(custom_user_agent="my-custom")
    """
    print("\n=== РУКОВОДСТВО ПО МИГРАЦИИ ===\n")
    print(migration_guide.__doc__)


if __name__ == "__main__":
    print("=" * 80)
    print("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ: User-Agent РЕЖИМЫ")
    print("=" * 80)

    example_compat_mode()
    example_safe_mode()
    example_safe_mode_with_service()
    example_safe_mode_with_user_data()
    example_custom_user_agent()
    show_priority_table()
    migration_guide()

    print("\n" + "=" * 80)
    print("Для использования с реальным Client, используйте async версии примеров")
    print("=" * 80)
