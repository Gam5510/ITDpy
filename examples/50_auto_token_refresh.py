# 50_auto_token_refresh.py
# Демонстрация автоматического обновления access_token

from itdpy import ITDClient

# Инициализируем клиент с refresh_token
client = ITDClient(refresh_token="your_refresh_token")

# ========================================
# 1. RequestHandler автоматически обновляет токен
# ========================================

# При получении 401 ошибки на любом запросе:
# - RequestHandler автоматически вызывает client._refresh_access_token()
# - Получает новый access_token
# - Повторяет запрос с новым токеном
# - Пользователь не замечает никаких изменений

# Пример: fetch posts (автоматический refresh на 401)
try:
    posts = client.posts.get_feed()
    print(f"Got {len(posts)} posts")
except Exception as e:
    print(f"Error: {e}")


# ========================================
# 2. Stream автоматически обновляет токен при переподключении
# ========================================

# При потере соединения:
# - Stream перезагружает новый access_token перед переподключением
# - Это гарантирует, что долгоживущие соединения работают бесконечно

stream = client.notifications.stream()


@stream.on("connected")
def on_connected(event):
    print("Connected to stream")
    # Токен был только что обновлен (если это переподключение)


@stream.on("notification")
def on_notification(event):
    print(f"Notification: {event.data.type}")


@stream.on("reconnecting")
def on_reconnecting(event):
    delay = event.data.get("delay")
    print(f"Reconnecting in {delay}s... (Token automatically refreshed)")


@stream.on("error")
def on_error(event):
    print(f"Stream error (will retry): {event.data.get('message')}")


# Запусти это - будет переподключаться бесконечно
# с автоматическим обновлением токена каждый раз
stream.run()

client.close()
