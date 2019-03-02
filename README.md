# ecommerce
e-commerce is a chance for survival.

1)
git clone https://github.com/dcashier/ecommerce.git
cd ecommerce/
переключаемся на ветку с 3 питоном
git checkout python_3

2)
Собрать и запустить контейнер
sudo docker-compose up --build

выйти Ctrl + C

3)
зайти в контейнер можно 2-мя способами

sudo docker-compose run web bash

или

зайти вполученный контейнер 66d57680a794
sudo docker exec -it 66d57680a794 bash

4)
Выполнить внутри контейнера

./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser

выйти из  контенера

5)
Снова запустить
sudo docker-compose up --build

6)
В браузере открыть ссылку
http://0.0.0.0:8000/
