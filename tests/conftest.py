import os
from urllib.parse import quote_plus
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import InvalidSessionIdException
from dotenv import load_dotenv
from selene import browser
import utils.allure_attach as attach

load_dotenv()


# Фикстура для настройки браузера
@pytest.fixture(scope="function", autouse = True)
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

#    options = Options()
#    service = ChromeService()


    # Получаем логин, пароль и URL из .env
    selenoid_login = os.getenv("SELENOID_LOGIN")
    selenoid_pass = os.getenv("SELENOID_PASS")
    selenoid_url = os.getenv("SELENOID_URL")
    encoded_pass = quote_plus(selenoid_pass)


    # Подключаем удалённый WebDriver через авторизацию
    driver = webdriver.Remote(
        command_executor=f"https://{selenoid_login}:{encoded_pass}@{selenoid_url}/wd/hub",
        options=options
    )

    driver.set_window_size(1920, 1080)  # Масштаб экрана (ширина x высота)

    # Применяем настройки к selene
    browser.config.driver = driver
    browser.config.type_by_js = True
    browser.config.window_height = 2500
    browser.config.window_width = 1400

    yield driver  # Передаем управление тесту

    try:
        print(attach.__file__)
        attach.add_html(browser)
        attach.add_screenshot(browser)
        attach.add_logs(browser)
        attach.add_video(browser)
    except Exception as e:
        print(f"Ошибка при прикреплении Allure-артефактов: {e}")

        # Только потом — закрываем браузер
    try:
        if driver.session_id:  # защита от повторного закрытия
            driver.quit()
    except InvalidSessionIdException:
        pass

    try:
        browser.quit()
    except InvalidSessionIdException:
        pass

