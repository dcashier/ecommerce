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


./manage.py shell

from eactor.models import *
from eshop.models import *
from eseller.models import *
from eloyalty.models import *

brand_1 = Brand(title=u"Базовый")
brand_1.save()
product_1 = Product(title="Позиция для списывания суммы", brand=brand_1)
product_1.save()

shop_1 = Shop(title=u"main shop", size="s")
shop_1.save()

seller_1 = Seller(shop=shop_1)
seller_1.save()

region_center = Region(title=u"Центральный")
region_center.save()
city_moscow = City(title=u"Moscow", region=region_center)
city_moscow.save()
pickup_point = PickupPoint(title=u"pickup 1", city=city_moscow)
pickup_point.save()

seller_1.pickup_points.add(pickup_point)

actor_1 = Actor(phone_number="dcashier_1@yandex.ru", is_person=True, seller=seller_1)
actor_1.save()
actor_1.set_password('12345q')

srl = ServiceRepositoryLoyalty()
title = "Roga i Kopita"
max_percent = 50
start_ball = 1000000
start_ball_available_day = 20000
reward_percent = 10
available_day =90
is_need_auth = True
srl.create_loyalty(seller_1, shop_1, title, max_percent, start_ball, start_ball_available_day, reward_percent, available_day, is_need_auth)



выйти из  контенера

5)
Снова запустить
sudo docker-compose up --build

6)
В браузере открыть ссылку
http://0.0.0.0:8000/
