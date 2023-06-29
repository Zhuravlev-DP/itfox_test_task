![workflow status](https://github.com/Zhuravlev-DP/itfox_test_task/actions/workflows/itfox_test_task.yml/badge.svg)

Проект доступен по адресу: http://158.160.106.232

Документация к API проекта: http://158.160.106.232/redoc/

### News Service
Предполагается аутентификация пользователей на основе токенов. Данный сервис предназначен для создания и просмотра новостей. Пользователи могут оставлять отзывы к новостям, ставить лайки.

#### Что могут делать авторизованные пользователи
- Выполнить аутентификацию под своим логином и паролем.
- Просматривать списки всех новостей, отдельной новости.
- Создавать/редактировать/удалять собственные новости.
- Просматривать списки всех комментариев, отдельного комментария.
- Создавать/удалять собственные комментари, комментарии к собственным новостям.
- Создавать/удалять собственные лайки.
#### Что может делать администратор
Администратор обладает всеми правами авторизованного пользователя.
Плюс к этому он может:
- редактировать/удалять любые новости,
- удалять любые комментарии.

#### Запуск проекта в контейнерах

- Клонирование удаленного репозитория
```bash
git clone git@github.com:Zhuravlev-DP/itfox_test_task.git
cd infra
```
- В директории /infra создайте файл .env, с переменными окружения, используя образец [.env.example](infra/.env.example)
- Сборка и развертывание контейнеров
```bash
docker-compose up -d --build
```
- Выполните миграции, соберите статику, создайте суперпользователя
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --no-input
docker-compose exec web python manage.py createsuperuser
```
- Стандартная админ-панель Django доступна по адресу [`https://localhost/admin/`](https://localhost/admin/)
- Документация к проекту доступна по адресу [`https://localhost/api/docs/`](`https://localhost/redoc/`)

#### Запуск API проекта в dev-режиме

- Клонирование удаленного репозитория (см. выше)
- в файле itfox_test_task/itfox_test_task/setting.py замените БД на встроенную SQLite
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
- Создание виртуального окружения и установка зависимостей
```bash
python -m venv venv (windows)
python3 -m venv venv (linux)
. source venv/Scripts/activate (windows)
. source venv/bin/activate (linux)
pip install --upgade pip
pip install -r -requirements.txt
```
- Примените миграции, соберите статику, создайте суперпользователя
```bash
cd itfox_test_task
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```
- Запуск сервера
```bash
python manage.py runserver
```
- Тестовые данные пользователей занесены в базу данных. Пользователю необходимо отправлять токен в загаловке каждого запроса. Получить токен через /api/v1/auth/ согласно документации. Также вы можете создать нового пользователя через админ-панель.
```
Данные админа:
    "username": "root"
    "password": "root"

Данные пользователей:
    "username": "max"
    "password": "max1234567890"

    "username": "vasya"
    "password": "vasya1234567890"
```