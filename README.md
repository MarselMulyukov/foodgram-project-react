##Продуктовый помощник. Диплом курса python-backend Я.Парктикум
[![Django-app workflow](https://github.com/MarselMulyukov/foodgram-project-react/actions/workflows/foodgram-workflow.yml/badge.svg)](https://github.com/MarselMulyukov/foodgram-project-react/actions/workflows/foodgram-workflow.yml)

#Доступен по адресу http://51.250.107.67/.
Для тестирования админки перейти на http://51.250.107.67/admin/
ввести логин - mulyu; и пароль - mars1987

#Возможности сервиса:
создание своей учетной записи
публикация рецептов и просмотр других
добавление рецептов в избранное
подписка на авторов
добавление рецептов в список покупок
скачивание списка необходимых продуктов для рецептов из списка покупок
административная панель с возможностью редактирования сущностей

#Проект  также готов для запуска на локальной машине:
1. Склонировать репозиторий git clone https://github.com/MarselMulyukov/foodgram-project-react.git
2. Перейти в директорию с инфраструктурой cd foodgram-project-react/infra
3. Создать .env файл с переменными окружения по примеру example.env
4. Выполнить команду docker-compose -d --build
5. Выполнить команду docker-compose exec backend python manage.py migrate
6. Выполнить команду docker-compose exec backend python manage.py collectstatic
7. Выполнить команду docker-compose exec backend python manage.py loaddata fixtures.json
8. Проект должен быть доступен по адресу localhost/
9. Админка должна быть доступна по адресу localhost/admin/

##Технологии и требования
Python 3.6+
Django 2.2.19
Django REST Framework 3.13
Django Filters
Docker