import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from pages.login_page import LoginPage


load_dotenv()


@pytest.fixture
def driver() -> WebDriver:
    """Создаёт браузер Chrome для UI-теста."""
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    yield driver

    driver.quit()


@pytest.fixture
def logged_in_driver(driver: WebDriver) -> WebDriver:
    """Открывает YouGile и выполняет авторизацию."""
    login_page = LoginPage(driver)

    login_page.open()
    login_page.login()

    board_url = os.getenv("YOUGILE_BOARD_URL")

    if not board_url:
        raise RuntimeError(
            "YOUGILE_BOARD_URL не найден в .env"
        )

    driver.get(board_url)

    return driver
