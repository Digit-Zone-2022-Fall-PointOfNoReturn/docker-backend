# Docker backend
Docker backend - это бэкенд часть сервиса, которая отвечает за хранение информации Telegram бота, а также предоставляет информацию, заложенную через админ-панель фреймворка [Django](https://www.djangoproject.com).

Исходя из названия, можно догадаться, что в своей основе бэкенд использует [Docker](https://www.docker.com/). Хотим обратить ваше внимание, что при разработке использовались последние версии `Docker`, а также `Docker Compose` (v2, которая является плагином).

Подробные инструкции по установке последних версий доступны здесь: [**ссылка на инструкцию для Ubuntu**](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/How-to-install-Docker-and-docker-compose-on-Ubuntu).

## Технологии
В основе комбинированного контейнера лежат следующие сервисы: `Docker`, `PostgreSQL`, а также `Nginx` (последние два в представлении не нуждаются, поэтому ссылки будут опущены).

## Установка
Для установки вам понадобится `Docker`, а также `Docker Compose` последних версий. Описание их установки будет опущено.
1. Клонируйте репозиторий с помощью команды `git clone https://github.com/Digit-Zone-2022-Fall-PointOfNoReturn/docker-backend.git`
2. Перейдите в соответствующую папку `cd docker-backend`
3. Запустите `Docker`, или убедитесь что он работает.
    
    *P.S. Некоторые советуют вручную запустить демона с помощью `sudo service docker start`, но этот момент мы также оставляем на вас.*
4. Опционально: замените файл `.env`, который отвечает за переменные окружения.

    *P.S. В последних коммитах данный файл будет лежать в папке и иметь значения, которые отвечают требованиям на рабочей версии сервиса.*
5. Запустите сервисы при помощи: `docker compose up -d --build`
6. Вы великолепны!

Сразу после старта, сервисы будут подниматься в следующем порядке: `PostgreSQL`, `Django`, `Nginx`.
`PostgreSQL` создаст необходимую базу данных и пользователя из переменных окружений, затем запуститься инициализирующий скрипт `Django` из папки `django/scripts`, который выполнит миграции и соберет статические файлы (далее создастся файл блокировки в папке `django/blocking`, его удаление повлечет новую итерацию миграций и сбора статики при поднятии контейнера, что может быть удобным).

## Дополнительные материалы
В основе API сервиса лежит `Django Rest Framework`, а также описание API в папке `django/apps` (по файлу на приложение). По этой причине можно ознакомиться с работой API просмотрев файлы или перейдя по ссылкам (так вы попадете в `DRF`).
