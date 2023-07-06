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
git clone git@github.com:Zhuravlev-DP/news_service.git
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
- Документация к проекту доступна по адресу [`https://localhost/api/docs/`](https://localhost/redoc/)

#### Запуск API проекта в dev-режиме

- Клонирование удаленного репозитория (см. выше)
- в файле news_service/news_service/setting.py замените БД на встроенную SQLite
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
cd news_service
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```
- Запуск сервера
```bash
python manage.py runserver
```
