import os
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote_plus
import pytest
from selenium import webdriver
from selene import browser
from dotenv import load_dotenv
import utils.allure_attach as attach

# Загрузка переменных окружения из файла .env
load_dotenv()

# Загрузка конфигураций из .env
SELENOID_LOGIN = os.getenv("SELENOID_LOGIN")
SELENOID_PASS = os.getenv("SELENOID_PASS")
SELENOID_URL = os.getenv("SELENOID_URL")
ENCODED_PASS = quote_plus(SELENOID_PASS)

# Проверка, что все необходимые переменные окружения были загружены
if not all([SELENOID_LOGIN, SELENOID_PASS, SELENOID_URL]):
    raise ValueError("Отсутствуют необходимые переменные окружения: SELENOID_LOGIN, SELENOID_PASS, или SELENOID_URL")

# Фикстура для WebDriver, которая запускает новый экземпляр браузера для каждого теста
@pytest.fixture(scope="function")
def driver():
    # Настройка опций для браузера
    options = Options()
    options.page_load_strategy = "eager"
    options.set_capability("browserName", "chrome")
    options.set_capability("browserVersion", "128.0")
    options.set_capability("selenoid:options", {
        "enableVNC": True,
        "enableVideo": True
    })

    # Подключение удалённого WebDriver через авторизацию
    driver = webdriver.Remote(
        command_executor=f"https://{SELENOID_LOGIN}:{ENCODED_PASS}@{SELENOID_URL}/wd/hub",
        options=options
    )

    # Установка базового URL для проекта
    browser.config.base_url = "https://crm.protei.ru/crm/crm.html#login"

    # Применение настроек к Selene
    browser.config.driver = driver
    browser.config.type_by_js = True
    browser.config.window_height = 2500
    browser.config.window_width = 1400

    # Передаем управление тесту
    yield driver

    # Прикрепление артефактов после выполнения теста
    try:
        if driver.session_id:  # Проверяем, что сессия активна
            print(attach.__file__)  # Для отладки, чтобы видеть путь к модулю
            attach.add_html(browser)
            attach.add_screenshot(browser)
            attach.add_logs(browser)
            attach.add_video(browser)
    except Exception as e:
        print(f"Ошибка при прикреплении артефактов: {e}")

    # Закрытие браузера после выполнения теста
    driver.quit()
