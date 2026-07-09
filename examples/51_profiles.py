# 51_profiles.py
# Демонстрация сохранения и переиспользования профиля (мульти-аккаунт)

from itdpy import ITDClient

# Первый запуск: передаём refresh_token/email+password и имя профиля.
# Клиент сам сохранит refresh_token, access_token и время его истечения
# в ~/.itdpy/profiles.json (Windows: %USERPROFILE%\.itdpy\profiles.json).
client = ITDClient(
    refresh_token="your_refresh_token",
    profile="main",
    auto_refresh_interval=None,
)
print("Access token истекает:", client.access_expires_at)
client.close()

# Повторный запуск (например, следующий старт приложения): достаточно
# указать только profile= — если сохранённый access_token ещё не истёк,
# refresh_token/email/password передавать не нужно.
client = ITDClient(profile="main", auto_refresh_interval=None)
print("Переиспользовали профиль, refresh_token:", client.refresh_token)
client.close()
