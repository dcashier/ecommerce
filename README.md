# ecommerce
e-commerce is a chance for survival.

Собрать и запустить контейнер
sudo docker-compose up --build

выйти Ctrl + C

зайти в контейнер можно 2-мя способами

sudo docker-compose run web bash

или

зайти вполученный контейнер 66d57680a794
sudo docker exec -it 66d57680a794 bash

Выполнить внутри контейнера

./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser

выйти из  контенера

Снова запустить
sudo docker-compose up --build

В браузере открыть ссылку
http://0.0.0.0:8000/
