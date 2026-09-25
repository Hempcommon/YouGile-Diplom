import uuid

import allure
import pytest
from pages.board_page import BoardPage


pytestmark = pytest.mark.ui


@allure.title("UI-001 Создание задачи")
@allure.story("Функциональность доски YouGile")
def test_create_task(logged_in_driver) -> None:
    """Проверяет создание новой задачи."""
    board = BoardPage(logged_in_driver)

    task_title = f"UI тест создание {uuid.uuid4().hex[:8]}"

    with allure.step("Создать новую задачу"):
        board.create_task("Новые", task_title)

    with allure.step("Проверить наличие созданной задачи"):
        assert board.is_task_present(task_title)


@allure.title("UI-002 Переименование задачи")
@allure.story("Функциональность доски YouGile")
def test_rename_task(logged_in_driver) -> None:
    """Проверяет изменение названия задачи."""
    board = BoardPage(logged_in_driver)

    old_title = f"UI тест переименование {uuid.uuid4().hex[:8]}"
    new_title = f"UI тест переименовано {uuid.uuid4().hex[:8]}"

    with allure.step("Создать тестовую задачу"):
        board.create_task("Новые", old_title)

    with allure.step("Переименовать задачу"):
        board.rename_task(old_title, new_title)

    with allure.step("Проверить новое название"):
        assert board.is_task_present(new_title)

    with allure.step("Удалить тестовую задачу"):
        board.delete_task(new_title)


@allure.title("UI-003 Перемещение задачи")
@allure.story("Функциональность доски YouGile")
def test_move_task(logged_in_driver) -> None:
    """Проверяет перемещение задачи между колонками."""
    board = BoardPage(logged_in_driver)

    task_title = f"UI тест перемещение {uuid.uuid4().hex[:8]}"

    with allure.step("Создать тестовую задачу"):
        board.create_task("Новые", task_title)

    with allure.step("Переместить задачу в колонку «В работе»"):
        board.move_task(task_title, "В работе")

    with allure.step("Обновить страницу"):
        board.refresh()

    with allure.step("Проверить наличие задачи после перемещения"):
        assert board.is_task_present(task_title)

    with allure.step("Удалить тестовую задачу"):
        board.delete_task(task_title)


@allure.title("UI-004 Создание колонки")
@allure.story("Функциональность доски YouGile")
def test_create_column(logged_in_driver) -> None:
    """Проверяет создание новой колонки."""
    board = BoardPage(logged_in_driver)

    column_name = f"UI колонка {uuid.uuid4().hex[:8]}"

    with allure.step("Создать новую колонку"):
        board.create_column(column_name)

    with allure.step("Проверить наличие новой колонки"):
        assert board.is_task_present(column_name) or (
            board._text_element(column_name) is not None
        )


@allure.title("UI-005 Удаление задачи")
@allure.story("Функциональность доски YouGile")
def test_delete_task(logged_in_driver) -> None:
    """Проверяет удаление задачи."""
    board = BoardPage(logged_in_driver)

    task_title = f"UI тест удаление {uuid.uuid4().hex[:8]}"

    with allure.step("Создать тестовую задачу"):
        board.create_task("Новые", task_title)

    with allure.step("Проверить создание задачи"):
        assert board.is_task_present(task_title)

    with allure.step("Удалить задачу"):
        board.delete_task(task_title)

    with allure.step("Проверить удаление задачи"):
        assert not board.is_task_present(task_title)


@allure.title("UI-006 Сохранение задачи после обновления")
@allure.story("Функциональность доски YouGile")
def test_task_persists_after_refresh(logged_in_driver) -> None:
    """Проверяет сохранение задачи после обновления страницы."""
    board = BoardPage(logged_in_driver)

    task_title = f"UI тест обновление {uuid.uuid4().hex[:8]}"

    with allure.step("Создать тестовую задачу"):
        board.create_task("Новые", task_title)

    with allure.step("Обновить страницу"):
        board.refresh()

    with allure.step("Проверить сохранение задачи"):
        assert board.is_task_present(task_title)

    with allure.step("Удалить тестовую задачу"):
        board.delete_task(task_title)
