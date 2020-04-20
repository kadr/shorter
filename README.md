# Сокращаетль ссылок

Для запуска проект, в корне проекта выполнить 
docker-compose up --build
После того как прокт успешно соберется: 
- форма будет доступна по адресу: http://localhost/
- Админка по адресу http://0.0.0.0:8000/admin/
- Api вьюха urls - http://0.0.0.0:8000/api/url/
- Api вьюха user - http://0.0.0.0:8000/api/user/

Для доступа в админку нужно создать суперпользователя: 
docker-compose exec web python  manage.py createsuperuser
