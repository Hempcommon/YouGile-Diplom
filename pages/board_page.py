import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BoardPage:
    """Страница доски YouGile."""

    def __init__(self, driver: WebDriver) -> None:
        """Инициализирует страницу доски."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def _find_column(self, column_name: str) -> WebElement:
        """Находит колонку по названию."""
        locator = (
            By.XPATH,
            (
                "//div[@data-testid='board-column']"
                "[.//span[normalize-space()="
                f"'{column_name}']]"
            ),
        )

        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    def _find_task(self, task_title: str) -> WebElement:
        """Находит карточку задачи."""
        locator = (
            By.XPATH,
            (
                "//div[@data-testid='tw-task-container']"
                "[.//div[@data-testid='board-task-title']"
                f"[contains(normalize-space(), '{task_title}')]]"
            ),
        )

        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    def _text_element(
        self,
        text: str,
    ) -> WebElement | None:
        """Находит видимый элемент с указанным текстом."""
        elements = self.driver.find_elements(
            By.XPATH,
            f"//*[normalize-space()='{text}']",
        )

        for element in elements:
            try:
                if element.is_displayed():
                    return element
            except Exception:
                continue

        return None

    def _task_exists_in_column(
        self,
        task_title: str,
        column_name: str,
    ) -> bool:
        """Проверяет наличие задачи в указанной колонке."""
        try:
            column = self._find_column(column_name)

            locator = (
                By.XPATH,
                (
                    ".//div[@data-testid='tw-task-container']"
                    "[.//div[@data-testid='board-task-title']"
                    f"[contains(normalize-space(), '{task_title}')]]"
                ),
            )

            column.find_element(*locator)
            return True

        except Exception:
            return False

    def _find_popup_project(self) -> WebElement:
        """Находит проект в окне «Размещение на доске»."""

        project_name = (
            "Дипломная работа - тестирование YouGile"
        )

        def find_project(
            driver: WebDriver,
        ) -> WebElement | bool:
            elements = driver.find_elements(
                By.XPATH,
                (
                    "//div["
                    "contains(@class, 'ml-4') and "
                    "contains(@class, 'text-no-wrap') and "
                    f"normalize-space()='{project_name}'"
                    "]"
                ),
            )

            for element in elements:
                try:
                    if not element.is_displayed():
                        continue

                    rect = element.rect

                    # Проект в левом меню расположен левее.
                    # Нужный проект находится в popup.
                    if rect["x"] < 240:
                        continue

                    return element

                except Exception:
                    continue

            return False

        return self.wait.until(find_project)

    def _click_project_arrow(
        self,
        project_text: WebElement,
    ) -> None:
        """
        Нажимает на стрелку проекта.

        Стрелка в HTML представлена SVG + path.
        У SVG нет обычного метода click(), поэтому
        отправляем мышиные события с bubbling.
        """

        path_d = (
            "M10.5303 7.46967C10.2374 7.17678 "
            "9.76256 7.17678 9.46967 7.46967C9.17678 "
            "7.76256 9.17678 8.23744 9.46967 8.53033L10.5303 "
            "7.46967ZM14 12L14.5303 12.5303C14.8232 "
            "12.2374 14.8232 11.7626 14.5303 11.4697L14 12ZM"
            "9.46967 15.4697C9.17678 15.7626 9.17678 "
            "16.2374 9.46967 16.5303C9.76256 16.8232 "
            "10.2374 16.8232 10.5303 16.5303L9.46967 "
            "15.4697ZM9.46967 8.53033L13.4697 12.5303L"
            "14.5303 11.4697L10.5303 7.46967L9.46967 "
            "8.53033ZM13.4697 11.4697L9.46967 "
            "15.4697L10.5303 16.5303L14.5303 "
            "12.5303L13.4697 11.4697Z"
        )

        arrow = project_text.find_element(
            By.XPATH,
            (
                "./ancestor::div["
                f".//*[name()='path' and @d=\"{path_d}\"]"
                "][1]"
                f"//*[name()='path' and @d=\"{path_d}\"]"
            ),
        )

        svg = arrow.find_element(
            By.XPATH,
            "./ancestor::*[name()='svg'][1]",
        )

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'center'
            });
            """,
            svg,
        )

        self.driver.execute_script(
            """
            const element = arguments[0];

            const events = [
                'pointerdown',
                'mousedown',
                'pointerup',
                'mouseup',
                'click'
            ];

            for (const eventName of events) {
                element.dispatchEvent(
                    new MouseEvent(
                        eventName,
                        {
                            bubbles: true,
                            cancelable: true,
                            view: window
                        }
                    )
                );
            }
            """,
            svg,
        )

    def _find_popup_item(
        self,
        text: str,
    ) -> WebElement:
        """Находит пункт в окне перемещения."""

        def find_item(
            driver: WebDriver,
        ) -> WebElement | bool:
            elements = driver.find_elements(
                By.XPATH,
                f"//*[normalize-space()='{text}']",
            )

            candidates = []

            for element in elements:
                try:
                    if not element.is_displayed():
                        continue

                    rect = element.rect

                    # Отбрасываем элементы левой панели.
                    if rect["x"] < 240:
                        continue

                    candidates.append(element)

                except Exception:
                    continue

            if not candidates:
                return False

            return candidates[-1]

        return self.wait.until(find_item)

    def _popup_item_exists(
        self,
        text: str,
    ) -> bool:
        """Проверяет наличие пункта в popup."""
        try:
            self._find_popup_item(text)
            return True
        except Exception:
            return False

    @allure.step(
        "Создать задачу в колонке «{column_name}»"
    )
    def create_task(
        self,
        column_name: str,
        task_title: str,
    ) -> None:
        """Создаёт задачу."""

        column = self._find_column(column_name)

        with allure.step("Найти «Добавить задачу»"):
            add_task = self.wait.until(
                lambda driver: column.find_element(
                    By.CSS_SELECTOR,
                    "[data-testid='link-button-new']",
                )
            )

        with allure.step("Нажать «Добавить задачу»"):
            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center'
                });
                """,
                add_task,
            )

            add_task.click()

        with allure.step("Ввести название задачи"):
            task_input = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "[data-testid='board-task-input-name']",
                    )
                )
            )

            task_input.clear()
            task_input.send_keys(task_title)

        with allure.step("Создать задачу"):
            task_input.send_keys(Keys.ENTER)

        with allure.step(
            "Проверить создание задачи"
        ):
            self.wait.until(
                lambda driver: self.is_task_present(
                    task_title
                )
            )

    @allure.step("Переименовать задачу")
    def rename_task(
        self,
        old_title: str,
        new_title: str,
    ) -> None:
        """Переименовывает задачу."""

        task = self._find_task(old_title)

        with allure.step("Открыть задачу"):
            task.click()

        with allure.step("Найти поле названия"):
            title_input = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "[data-testid='board-task-input-name']",
                    )
                )
            )

        with allure.step("Изменить название"):
            title_input.click()
            title_input.clear()
            title_input.send_keys(new_title)
            title_input.send_keys(Keys.ENTER)

        with allure.step(
            "Проверить новое название"
        ):
            self.wait.until(
                lambda driver: self.is_task_present(
                    new_title
                )
            )

    @allure.step("Переместить задачу")
    def move_task(
        self,
        task_title: str,
        to_column: str,
    ) -> None:
        """Перемещает задачу через меню YouGile."""

        task = self._find_task(task_title)

        with allure.step("Открыть меню задачи"):
            menu_button = self.wait.until(
                lambda driver: task.find_element(
                    By.CSS_SELECTOR,
                    "[data-testid='board-task-menu']",
                )
            )

            menu_button.click()

        with allure.step("Нажать «Переместить»"):
            move_button = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//*[normalize-space()='Переместить']",
                    )
                )
            )

            move_button.click()

        with allure.step(
            "Нажать «Указать место назначения...»"
        ):
            destination_button = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//*[normalize-space()="
                        "'Указать место назначения...']",
                    )
                )
            )

            destination_button.click()

        with allure.step(
            "Дождаться окна «Размещение на доске»"
        ):
            self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//*[normalize-space()="
                        "'Размещение на доске']",
                    )
                )
            )

        with allure.step(
            "Найти проект "
            "«Дипломная работа - тестирование YouGile»"
        ):
            project_text = self._find_popup_project()

        with allure.step(
            "Нажать стрелку справа от проекта"
        ):
            self._click_project_arrow(project_text)

        with allure.step(
            "Дождаться появления «Новая доска»"
        ):
            self.wait.until(
                lambda driver: self._popup_item_exists(
                    "Новая доска"
                )
            )

        with allure.step(
            "Выбрать доску «Новая доска»"
        ):
            board_button = self._find_popup_item(
                "Новая доска"
            )

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center',
                    inline: 'center'
                });
                """,
                board_button,
            )

            board_button.click()

        with allure.step(
            f"Дождаться колонки «{to_column}»"
        ):
            self.wait.until(
                lambda driver: self._popup_item_exists(
                    to_column
                )
            )

        with allure.step(
            f"Выбрать колонку «{to_column}»"
        ):
            column_button = self._find_popup_item(
                to_column
            )

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center',
                    inline: 'center'
                });
                """,
                column_button,
            )

            column_button.click()

        with allure.step(
            "Проверить перемещение задачи"
        ):
            self.wait.until(
                lambda driver: self._task_exists_in_column(
                    task_title,
                    to_column,
                )
            )

    @allure.step("Создать колонку")
    def create_column(
        self,
        column_name: str,
    ) -> None:
        """Создаёт новую колонку."""

        with allure.step(
            "Найти кнопку «Создать колонку»"
        ):
            add_column = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[@role='button']"
                        "[.//span[normalize-space()="
                        "'Создать колонку']]",
                    )
                )
            )

        with allure.step(
            "Нажать «Создать колонку»"
        ):
            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center'
                });
                """,
                add_column,
            )

            add_column.click()

        with allure.step(
            "Найти поле названия колонки"
        ):
            column_input = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//*[self::input or self::textarea]"
                        "[contains(@placeholder, "
                        "'Введите имя колонки')]",
                    )
                )
            )

        with allure.step(
            "Ввести название колонки"
        ):
            column_input.clear()
            column_input.send_keys(column_name)

        with allure.step("Создать колонку"):
            column_input.send_keys(Keys.ENTER)

        with allure.step(
            "Проверить создание колонки"
        ):
            self.wait.until(
                lambda driver: self._column_exists(
                    column_name
                )
            )

    def _column_exists(
        self,
        column_name: str,
    ) -> bool:
        """Проверяет наличие колонки."""

        try:
            locator = (
                By.XPATH,
                (
                    "//div[@data-testid='board-column']"
                    "[.//span[normalize-space()="
                    f"'{column_name}']]"
                ),
            )

            self.wait.until(
                EC.visibility_of_element_located(
                    locator
                )
            )

            return True

        except Exception:
            return False

    @allure.step("Обновить страницу")
    def refresh(self) -> None:
        """Обновляет страницу."""

        self.driver.refresh()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "[data-testid='board-column']",
                )
            )
        )

    @allure.step(
        "Удалить задачу «{task_title}»"
    )
    def delete_task(
        self,
        task_title: str,
    ) -> None:
        """Удаляет задачу."""

        task = self._find_task(task_title)

        with allure.step("Открыть меню задачи"):
            menu_button = self.wait.until(
                lambda driver: task.find_element(
                    By.CSS_SELECTOR,
                    "[data-testid='board-task-menu']",
                )
            )

            menu_button.click()

        with allure.step("Нажать «Удалить»"):
            delete_button = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[normalize-space()='Удалить']",
                    )
                )
            )

            delete_button.click()

        with allure.step(
            "Подтвердить удаление"
        ):
            confirm_button = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "(//*[normalize-space()='Удалить'])"
                        "[last()]",
                    )
                )
            )

            confirm_button.click()

        with allure.step(
            "Проверить удаление задачи"
        ):
            self.wait.until(
                lambda driver: not self.is_task_present(
                    task_title
                )
            )

    @allure.step(
        "Проверить наличие задачи «{task_title}»"
    )
    def is_task_present(
        self,
        task_title: str,
    ) -> bool:
        """Проверяет наличие задачи."""

        locator = (
            By.XPATH,
            (
                "//div[@data-testid='tw-task-container']"
                "[.//div[@data-testid='board-task-title']"
                f"[contains(normalize-space(), "
                f"'{task_title}')]]"
            ),
        )

        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    locator
                )
            )

            return True

        except Exception:
            return False
