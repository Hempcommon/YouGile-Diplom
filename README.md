№Дипломная работа-тестирование YouGile

Проект содержит автотесты веб-приложения YouGile на Python с использованием pytest, Selenium, Requests и Allure.

##Что тестируется

UI-тесты проверяют основные действия с задачами и колонками на доске YouGile.

API-тесты проверяют основные GET-запросы YouGile API, а также негативные сценарии с отсутствующей авторизацией и несуществующим проектом.

Всего в проекте:
- 6 UI-автотестов
- 6 API-автотестов
- 12 автотестов в общем

##Требования

- Python 3.14+
- Google Chrome

##Установка

Перейдите в папку "diplom" и установите зависимости:

```powershell
python -m pip install -r requirements.txt
№=Перед запуском создайте файл .env в папке diplom и укажите необходимые переменные окружения:

YOUGILE_UI_URL=https://ru.yougile.com/
YOUGILE_BOARD_URL=https://ru.yougile.com/team/54dbfc22a43c/%D0%94%D0%B8%D0%BF%D0%BB%D0%BE%D0%BC%D0%BD%D0%B0%D1%8F-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0-__dash__-%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-YouGile/%D0%9D%D0%BE%D0%B2%D0%B0%D1%8F-%D0%B4%D0%BE%D1%81%D0%BA%D0%B0#ID-36
YOUGILE_API_BASE_URL=https://yougile.com/api-v2

YOUGILE_UI_EMAIL=your_email
YOUGILE_UI_PASSWORD=your_password
YOUGILE_API_TOKEN=your_token

##Запуск тестов

##Запустить только UI-тесты:

python -m pytest -m ui

##Запустить только API-тесты:

python -m pytest -m api

##Запустить все тесты:

python -m pytest
Allure

##Сгенерировать результаты для Allure:

python -m pytest tests --alluredir=allure-results

##Открыть Allure-отчёт:

allure serve allure-results

##Инструменты

Python, pytest, Selenium, Requests, Allure, Postman.

##Репозиторий GitHub



##Отчёт в Yonote

