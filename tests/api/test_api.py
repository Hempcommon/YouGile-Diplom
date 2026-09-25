import os

import allure
import pytest
import requests


BASE_URL = os.getenv("YOUGILE_API_BASE_URL")
TOKEN = os.getenv("YOUGILE_API_TOKEN")

if not BASE_URL:
    pytest.fail("YOUGILE_API_BASE_URL не найден в переменных окружения")

if not TOKEN:
    pytest.fail("YOUGILE_API_TOKEN не найден в переменных окружения")


@pytest.mark.api
@allure.title("Получение данных текущего пользователя")
@allure.story("API YouGile")
def test_get_current_user() -> None:
    """Проверяет получение данных текущего пользователя."""
    with allure.step("Отправить GET-запрос к /users/me"):
        response = requests.get(
            f"{BASE_URL}/users/me",
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json",
            },
            timeout=10,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 200


@pytest.mark.api
@allure.title("Получение списка проектов")
@allure.story("API YouGile")
def test_get_projects() -> None:
    """Проверяет получение списка проектов."""
    with allure.step("Отправить GET-запрос к /projects"):
        response = requests.get(
            f"{BASE_URL}/projects",
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json",
            },
            timeout=10,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 200


@pytest.mark.api
@allure.title("Получение списка досок")
@allure.story("API YouGile")
def test_get_boards() -> None:
    """Проверяет получение списка досок."""
    with allure.step("Отправить GET-запрос к /boards"):
        response = requests.get(
            f"{BASE_URL}/boards",
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json",
            },
            timeout=10,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 200


@pytest.mark.api
@allure.title("Получение списка задач")
@allure.story("API YouGile")
def test_get_tasks() -> None:
    """Проверяет получение списка задач."""
    with allure.step("Отправить GET-запрос к /tasks"):
        response = requests.get(
            f"{BASE_URL}/tasks",
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json",
            },
            timeout=10,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 200


@pytest.mark.api
@allure.title("Получение списка проектов без авторизации")
@allure.story("API YouGile")
def test_get_projects_without_authorization() -> None:
    """Проверяет запрет доступа к проектам без авторизации."""
    with allure.step("Отправить GET-запрос к /projects без токена"):
        response = requests.get(
            f"{BASE_URL}/projects",
            timeout=10,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 401


@pytest.mark.api
@allure.title("Получение несуществующего проекта")
@allure.story("API YouGile")
def test_get_nonexistent_project() -> None:
    """Проверяет обработку запроса несуществующего проекта."""
    nonexistent_project_id = "00000000-0000-0000-0000-000000000000"

    with allure.step("Отправить GET-запрос к несуществующему проекту"):
        response = requests.get(
            f"{BASE_URL}/projects/{nonexistent_project_id}",
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json",
            },
            timeout=10,
        )

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 404
