# dating_app

`dating_app` - это REST-API приложения знакомств.

## Системные требования
- Python 3.11+
- Works on Linux, Windows, macOS

## Технологии:
- Python 3.11
- Django 4
- Django REST Framework
- PostgreSQL
- Celery 
- RabbitMQ
- Nginx
- Gunicorn
- Docker & Docker compose

## Как запустить проект:

Для запуска в проект вложена конфигурация docker-compose. После запуска docker-compose API будет доступно по адресу: `http://<host address>/`

Необходимо выполнить следующие шаги:
- Склонируйте репозиторий с GitHub и перейдите в папку проекта, где расположен файл docker-compose.yml:

```
git clone https://github.com/KostKH/dating_app.git
cd dating_app/infra_dating/
```

- Проверьте, что на машине / сервере установлены `docker` и `docker compose`

- Cоздайте в папке `infra_dating` файл `.env` с переменными окружения. Можно создать его из вложенного образца `env_example.env`:
```
cp env_example.env .env
```
- Откройте файл .env в редакторе и поменяйте, при необходимости, переменные окружения. При этом обязательно поменяйте секретный ключ и пароли.

- Поменяйте хост на ваш в файле `nginx.conf`

- Установите и запустите приложение в контейнере. (Возможно, вам придется добавить `sudo` перед текстом команды):
```
docker compose up -d
```
- Запустите миграции, соберите статику, создайте суперпользоветеля:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic
```

## Эдпойнты и особенности их использования

Были созданы следущие эндпойнты:

#### Эндпойнты, доступные всем пользователям:
```
/api/clients/create/ - регистрация (POST)
/api/api-token-auth/ - получение токена (POST)
```
#### Эндпойнты, доступные только авторизованным пользователям:
```
/api/list/ - получение списка пользователей (GET)
/api/clients/<id>/match/ - лайк понравившегося пользователя (POST)
```

Для создания пользователя тело запроса должно включать поля:
- email
- first_name - Имя
- last_name - Фамилия,
- password - пароль,
- gender - пол, одной буквой - М или Ж,
- latitude - широта, в градусах, напр 56.6235, (по умолчанию - 54.9827385
- longitude - широта, в градусах, напр 56.6235, (по умолчанию - 82.8977945
- avatar - картинка в формате base64, напр.:
```
"avatar": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQA ... AOBRRRTEf/9k="
```

Для получения токена нужно в теле запроса передать email и пароль

Для доступа к эндпойнтам, требущим авторизации, нужно в заголовке запроса
передать параметр с ключом `Authorization` и значением `Token 350un3n4nm...0jn43`

В эндпойнте `/api/list/` доступны фильтры со следующими ключами:
- first_name - фильтр по имени
- last_name - фильтр по фамилии
- gender - фильтр по полу
- distance - фильтр по расстоянию (в км)

## О программе:

Автор: Константин Харьков
