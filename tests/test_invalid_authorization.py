from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selene import browser, have
import allure
from allure_commons.types import Severity


# Тест с использованием Selene
@allure.tag("web")
@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Nailia-Ales')
@allure.feature("Сборка Allure-отчета о тестировании в Jenkins")
@allure.story("Проверка валидации при неправильном вводе кред в форме авторизации (Selene)")
@allure.link('https://github.com/', 'Testing')
def test_invalid_authorization():

    # Шаг 1: Открытие страницы авторизации
    browser.open('https://crm.protei.ru/crm/crm.html#login')

    # Шаг 2: Ввод неверных данных в поле логина
    browser.element('input[id="gwt-debug-auth-input-login"]').type('user')

    # Шаг 3: Ввод неверных данных в поле пароля
    browser.element('input[id="gwt-debug-auth-input-password"]').type('1234')

    # Шаг 4: Нажатие кнопки "Войти"
    browser.element('button[id="gwt-debug-auth-login-button"]').click()

    # Шаг 5: Ожидание появления сообщения об ошибке и проверка текста ошибки
    browser.element('[class="alert alert-danger m-t-15 text-center"]').should(have.text('Ошибка! Неправильно указаны логин или пароль'))

    # Закрытие браузера
    browser.quit()


# Тест с использованием Selenium
@allure.tag("web")
@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Nailia-Ales')
@allure.feature("Сборка Allure-отчета о тестировании в Jenkins")
@allure.story("Проверка валидации при неправильном вводе кред в форме авторизации (Selenium)")
@allure.link('https://github.com/', 'Testing')
def test_invalid_authorization_selenium(driver):

    # Шаг 2: Открытие страницы авторизации
    driver.get('https://crm.protei.ru/crm/crm.html#login')

    # Шаг 3: Ввод неверных данных в поле логина
    login_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'gwt-debug-auth-input-login'))
    )
    login_input.send_keys('user')

    # Шаг 4: Ввод неверных данных в поле пароля
    driver.find_element(By.ID, 'gwt-debug-auth-input-password').send_keys('1234')

    # Шаг 5: Нажатие кнопки "Войти"
    driver.find_element(By.ID, 'gwt-debug-auth-login-button').click()

    # Шаг 6: Ожидание появления сообщения об ошибке
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'alert-danger'))
    )

    # Шаг 7: Проверка текста ошибки
    assert "Ошибка! Неправильно указаны логин или пароль" in error_message.text



# Тест с использованием Selenium и Fixture
@allure.tag("web")
@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Nailia-Ales')
@allure.feature("Сборка Allure-отчета о тестировании в Jenkins")
@allure.story("Проверка валидации при неправильном вводе кред в форме авторизации (Selenium + Fixture)")
@allure.link('https://github.com/', 'Testing')
def test_invalid_authorization_selenium_with_fixture(driver):
    # Шаг 1: Открытие страницы авторизации
    driver.get('https://crm.protei.ru/crm/crm.html#login')

    # Шаг 2: Ввод неверных данных в поле логина
    login_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'gwt-debug-auth-input-login'))
    )
    login_input.send_keys('user')

    # Шаг 3: Ввод неверных данных в поле пароля
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="gwt-debug-auth-input-password"]'))
    )
    password_input.send_keys('1234')

    # Шаг 4: Нажатие кнопки "Войти"
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[id="gwt-debug-auth-login-button"]'))
    )
    login_button.click()

    # Шаг 5: Ожидание появления сообщения об ошибке
    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[class="alert alert-danger m-t-15 text-center"]'))
    )

    # Шаг 6: Проверка текста ошибки
    assert "Ошибка! Неправильно указаны логин или пароль" in error_message.text
