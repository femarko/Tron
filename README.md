### Задача

Написать микросервис, который будет выводить информацию по адресу 
в сети трон, его bandwidth, energy, и баланс trx.\
Эндпоинт должен принимать входные данные - адрес.\
Каждый запрос писать в базу данных, с полями о том какой кошелек 
запрашивался.\
Написать юнит/интеграционные тесты

У сервиса 2 ендпоинта:
- POST
- GET для получения списка последних записей из БД, включая пагинацию,

2 теста:
- интеграционный на ендпоинт
- юнит на запись в бд

> Примечания: использовать FastAPI, аннотацию(typing), SQLAlchemy ORM, для удобства с взаимодействию с троном можно использовать tronpy, для тестов Pytest

```
./
├── Dockerfile
├── Makefile
├── README.md
├── docker-compose.yml
├── pytest.ini
├── requirements-dev.txt
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── application/
│   │   ├── __init__.py
│   │   ├── app_manager.py
│   │   ├── protocols.py
│   │   └── unit_of_work.py
│   ├── bootstrap/
│   │   ├── __init__.py
│   │   ├── bootstrap.py
│   │   ├── config.py
│   │   └── container.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── errors.py
│   │   └── models.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── orm/
│   │   │   ├── __init__.py
│   │   │   ├── adapters.py
│   │   │   ├── repo_impl.py
│   │   │   └── sql_aclchemy_wrapper.py
│   │   ├── reset_db.py
│   │   └── tron/
│   │       ├── __init__.py
│   │       └── tron_interface.py
│   └── interfaces/
│       ├── __init__.py
│       ├── cli/
│       │   ├── __init__.py
│       │   └── reset_db.py
│       └── fastapi_app/
│           ├── __init__.py
│           ├── main.py
│           ├── schemas.py
│           └── urls.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_app_manager.py
    ├── test_config.py
    ├── test_tron_interface.py
    └── test_web.py
```
