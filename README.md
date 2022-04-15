Продуктовый помощник. Диплом курса python-backend Я.Парктикум

Возможности сервиса:
создание своей учетной записи
публикация рецептов и просмотр других
добавление рецептов в избранное
подписка на авторов
добавление рецептов в список покупок
скачивание списка необходимых продуктов для рецептов из списка покупок
административная панель с возможностью редактирования сущностей

Проект готов для запуска на локальной машине:
1. Склонировать репозиторий git clone https://github.com/MarselMulyukov/foodgram-project-react.git
2. Перейти в директорию с инфраструктурой cd foodgram-project-react/infra
3. Создать .env файл с переменными окружения по примеру example.env
4. Выполнить команду docker-compose -d --build
5. Выполнить команду docker-compose exec backend python manage.py migrate
6. Выполнить команду docker-compose exec backend python manage.py collectstatic
7. Выполнить команду docker-compose exec backend python manage.py runscript loadingredients
8. Проект должен быть доступен по адресу localhost/
9. Админка должна быть доступна по адресу localhost/admin/