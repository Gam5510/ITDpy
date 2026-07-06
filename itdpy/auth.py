import logging
import os
import time

import requests

from .exceptions import (
    AuthenticationError,
    BrowserNotAvailableError,
    InvalidCredentialsError,
    TurnstileTimeoutError,
)

logger = logging.getLogger("itdpy.auth")

try:
    from DrissionPage import ChromiumPage, ChromiumOptions
except ImportError:
    ChromiumPage = None
    ChromiumOptions = None

try:
    from pyvirtualdisplay import Display
except ImportError:
    Display = None

_TURNSTILE_CONTAINER_LOCATORS = (
    "css:.cf-turnstile",
    "css:div[class*='turnstile']",
    "css:iframe[src*='challenges.cloudflare.com']",
    "xpath://iframe[contains(@src, \"challenges.cloudflare.com\")]",
)


def _try_click_turnstile_checkbox(page) -> bool:

    for locator in _TURNSTILE_CONTAINER_LOCATORS:
        try:
            ele = page.ele(locator, timeout=1)
        except Exception:
            ele = None
        if not ele:
            continue

        for offset_x, offset_y in ((-120, 0), (0, 0), (-100, -10)):
            try:
                page.actions.move_to(ele, offset_x=offset_x, offset_y=offset_y).click()
                return True
            except Exception:
                continue

        try:
            ele.click()
            return True
        except Exception:
            pass
    return False


_TURNSTILE_INTERCEPTOR_JS = """
window.capturedToken = null;
const originalFetch = window.fetch;

window.fetch = async function(...args) {
    const url = args[0];
    if (typeof url === 'string' && url.includes('sign-in')) {
        const options = args[1];
        if (options && options.body) {
            try {
                const payload = JSON.parse(options.body);
                if (payload.turnstileToken) {
                    window.capturedToken = payload.turnstileToken;
                }
            } catch (e) {}
        }
        return new Promise(() => {});
    }
    return originalFetch.apply(this, args);
};
"""


def login_with_password(
    email: str,
    password: str,
    *,
    base_url: str = "https://xn--d1ah4a.com",
    max_wait_time: int = 60,
    browser_path: str = None,
) -> str:
    if ChromiumPage is None:
        logger.error("DrissionPage не установлен")
        raise BrowserNotAvailableError(
            "DrissionPage не установлен. Установите его командой: pip install DrissionPage"
        )

    display = None
    if os.name == "posix" and Display is not None:
        try:
            display = Display(visible=0, size=(1920, 1080))
            display.start()
            logger.debug("Виртуальный дисплей Xvfb запущен")
        except Exception:
            logger.warning("Не удалось запустить виртуальный дисплей Xvfb", exc_info=True)
            display = None

    page = None
    try:
        options = ChromiumOptions()
        options.set_argument("--no-sandbox")
        options.set_argument("--disable-dev-shm-usage")
        if browser_path:
            options.set_browser_path(browser_path)

        logger.info("Запуск браузера для входа email=%s", email)
        try:
            page = ChromiumPage(addr_or_opts=options)
        except Exception as e:
            logger.error("Не удалось запустить браузер: %s", e, exc_info=True)
            raise BrowserNotAvailableError(
                f"Не удалось запустить браузер (проверьте, что Chrome/Chromium "
                f"установлен, либо укажите browser_path): {e}"
            ) from e

        page.get(f"{base_url}/login")
        page.wait.load_start()
        logger.debug("Страница логина загружена: %s/login", base_url)

        page.run_js(_TURNSTILE_INTERCEPTOR_JS)

        page.ele("css:input[type=email]").input(email)
        page.ele("css:input[type=password]").input(password)
        page.ele("@type=submit").click()
        logger.debug("Форма входа отправлена, ожидаем токен Turnstile")

        captured_token = None
        start_time = time.time()
        last_click_attempt = 0.0
        while time.time() - start_time < max_wait_time:
            captured_token = page.run_js("return window.capturedToken;")
            if captured_token:
                break
            now = time.time()
            if now - last_click_attempt >= 1.0:
                last_click_attempt = now
                if _try_click_turnstile_checkbox(page):
                    logger.debug("Кликнули по чекбоксу Turnstile")

            time.sleep(0.1)

        if not captured_token:
            logger.error(
                "Токен Turnstile не был перехвачен за %s сек", max_wait_time
            )
            raise TurnstileTimeoutError(
                f"Превышено время ожидания капчи Turnstile ({max_wait_time} сек)"
            )
        logger.debug("Токен Turnstile перехвачен")

        browser_cookies = page.cookies()
        page.quit()
        page = None

        session = requests.Session()
        for cookie in browser_cookies:
            session.cookies.set(cookie["name"], cookie["value"], domain=cookie["domain"])

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
            "Referer": f"{base_url}/login",
            "Content-Type": "application/json",
        }
        payload = {
            "email": email,
            "password": password,
            "turnstileToken": captured_token,
        }

        response = session.post(
            f"{base_url}/api/v1/auth/sign-in", json=payload, headers=headers
        )

        if not response.ok:
            error_code = None
            error_message = response.text
            try:
                error_data = response.json().get("error", {})
                error_code = error_data.get("code")
                error_message = error_data.get("message", error_message)
            except (ValueError, AttributeError):
                pass

            logger.error(
                "Ошибка входа для %s: HTTP %s code=%s message=%s",
                email, response.status_code, error_code, error_message,
            )

            if error_code == "INVALID_CREDENTIALS":
                raise InvalidCredentialsError(
                    f"Неверный email или пароль для {email}"
                )
            raise AuthenticationError(
                f"Ошибка входа: HTTP {response.status_code} {error_message}"
            )

        refresh_token = session.cookies.get("refresh_token")
        if not refresh_token:
            logger.error("Ответ на sign-in успешен, но refresh_token отсутствует в cookies")
            raise AuthenticationError("Не удалось получить refresh_token после входа")

        logger.info("Вход выполнен успешно для %s", email)
        return refresh_token
    finally:
        if page is not None:
            page.quit()
        if display is not None:
            display.stop()
