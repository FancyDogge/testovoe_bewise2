## Описание
### Тестовое задание от компании Bewise, задача 2:
Был реализован сервис, позволяющий создавать юзера, принимать аудиофайл в формате wav, форматировать его в mp3 и присваивать его определенному юзеру, генерируя url для его скачивания.
Также был реализован эндпоинт, который позволяет скачать запись по этому url.

Для реализации проекта были использованы следующие технологии: FastAPI, SQLAlchemy, Docker, PostgreSQL (полный список в requirements.txt).

## Инструкция по запуску
Для начала нужно клонировать данный репозиторий

```
git clone https://github.com/FancyDogge/testovoe_bewise2.git
```

Далее для запуска перейдите в директорию с docker-compose.yml и введите сдледующую команду для 

```
docker-compose up --build
```

Начнется сборка образов и установка зависимостей, после чего приложение и бд должны запуститься.
Миграции запустятся автоматически.

Все готово!
Теперь приложение запущено и можно опробовать API по адресу localhost:8000/docs
