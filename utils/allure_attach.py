import allure
from allure_commons.types import AttachmentType


# 📸 Скриншот текущего экрана браузера
def add_screenshot(browser):
    png = browser.driver.get_screenshot_as_png()
    allure.attach(
        body=png,
        name='Screenshot',
        attachment_type=AttachmentType.PNG,
        extension='.png'
    )


# 📜 Логи браузера
def add_logs(browser):
    logs = "\n".join(f'{log}' for log in browser.driver.get_log('browser'))

    # Экранирование спецсимволов
    logs = logs.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")

    allure.attach(
        logs,
        name='Browser Logs',
        attachment_type=AttachmentType.TEXT,
        extension='.log'
    )


# 🧾 HTML-код текущей страницы
def add_html(browser):
    html = browser.driver.page_source

    # Экранирование HTML символов
    html = html.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")

    allure.attach(
        html,
        name='Page Source',
        attachment_type=AttachmentType.HTML,
        extension='.html'
    )


# 🎥 Видео

def add_video(browser):
    video_url = "https://selenoid.autotests.cloud/video/" + browser.driver.session_id + ".mp4"
    html = "<html><body><video width='100%' height='100%' controls autoplay><source src=' " \
          + video_url \
          + " ' type='video/mp4'></video></body></html>"
    allure.attach(html, 'video_' + browser.driver.session_id, attachment_type=AttachmentType.HTML, extension='.html')

