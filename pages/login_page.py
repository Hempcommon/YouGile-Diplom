import os

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    """Страница авторизации YouGile."""

    def __init__(self, driver: WebDriver) -> None:
        """Инициализирует страницу авторизации."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    @allure.step("Открыть YouGile")
    def open(self) -> None:
        """Открывает главную страницу YouGile."""
        url = os.getenv("YOUGILE_UI_URL")

        if not url:
            raise RuntimeError(
                "YOUGILE_UI_URL не найден в переменных окружения"
            )

        self.driver.get(url)

    @allure.step("Выполнить авторизацию")
    def login(self) -> None:
        """Выполняет вход в аккаунт YouGile."""
        email = os.getenv("YOUGILE_UI_EMAIL")
        password = os.getenv("YOUGILE_UI_PASSWORD")

        if not email or not password:
            raise RuntimeError(
                "YOUGILE_UI_EMAIL или YOUGILE_UI_PASSWORD "
                "не найдены в переменных окружения"
            )

        with allure.step("Открыть форму авторизации"):
            login_link = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//*[normalize-space()='Войти']",
                    )
                )
            )
            login_link.click()

        with allure.step("Дождаться появления поля E-mail"):
            email_input = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//input[@type='email']",
                    )
                )
            )

        with allure.step("Ввести адрес электронной почты"):
            email_input.clear()
            email_input.send_keys(email)

        with allure.step("Ввести пароль"):
            password_input = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//input[@type='password']",
                    )
                )
            )
            password_input.clear()
            password_input.send_keys(password)

        with allure.step("Нажать кнопку «Войти»"):
            submit_button = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//form[contains(@class, 'login-form')]"
                        "//div[@role='button' "
                        "and .//div[normalize-space()='Войти']]",
                    )
                )
            )
            submit_button.click()

        with allure.step("Дождаться завершения авторизации"):
            self.wait.until(
                EC.invisibility_of_element_located(
                    (
                        By.XPATH,
                        "//form[contains(@class, 'login-form')]",
                    )
                )
            )
