import os
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote_plus
import pytest
from selenium import webdriver
from selene import browser
from dotenv import load_dotenv
import utils.allure_attach as attach


def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default='128.0'
    )


# Загрузка переменных окружения из файла .env
load_dotenv()

# Фикстура для WebDriver, которая запускает новый экземпляр браузера для каждого теста
@pytest.fixture(scope="function")
def driver(request):
    browser.config.base_url = "https://crm.protei.ru/crm/crm.html#login"
    # Настройка опций для браузера

    browser_version = request.config.getoption('--browser_version')


    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": f"{browser_version}",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }

    # Получаем логин, пароль и URL из .env
    selenoid_login = os.getenv("SELENOID_LOGIN")
    selenoid_pass = os.getenv("SELENOID_PASS")
    selenoid_url = os.getenv("SELENOID_URL")
    encoded_pass = quote_plus(selenoid_pass)

    # Подключаем удалённый WebDriver через авторизацию
    options.capabilities.update(selenoid_capabilities)
    driver = webdriver.Remote(
        command_executor=f"https://{selenoid_login}:{encoded_pass}@{selenoid_url}/wd/hub",
        options=options
    )


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
