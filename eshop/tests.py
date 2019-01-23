#!-*-coding: utf-8 -*-
from django.test import TestCase

from eshop.models import *
from django.test.client import Client
import json
import sys
import time
import pprint
from decimal import Decimal

# Create your tests here.

class TestEShop(TestCase):
    def setUp(self):
        print "SETUP DATA FOR ..."
        self.assertEqual.__self__.maxDiff = None

        #catalog_shops = CatalogShops(title=u"main catalog")
        #catalog_shops.save()

    def test_1(self):
        """
        Сейчас 2020.12.23 пред новогодние распродажи.
        Вова живет в Крыиу(в Алуште), и хочет себе новый телефон. Выбирает между Apple и Samsung. За телеофном готов сьездить и в Ялту и в Семфирополь.

        Компания E-commerce имеет две point_pickup в Симферополе, одну в Ялте, две в Севастополе, пятьдесят три в Москве, а на своих складах в Москве Сочи и Симферополе телефоны Apple LG Samsung Nokia разных моделей в большом колличестве.
        Однако не может продавать Apple на всей территории Крыма начиная с 2017 года.
        Устраивает акции по покупке телфона самсунг Note9 с чехлом в Ялте(там точка самовыоза) сумма будет 101000.
        Хотя если покупать телефон Note9 отдельно он стоит 100000, а чехол стоит 5000.
        При online оплате во всей России на любые телфоны скидка 2%.
        Компания пока не опреллилась сумируются акции или нет. (рассмотрим что акции не суммируются)

        Есть корпоративный клиент.

        Есть еще одна окмпания, опишем :
        shop = {title: 'Компания J-commerce'}
        pickup_points = [ # точки самовывоза
            {city: 'Симферополь'},
            {city: 'Москва'},
        ]
        products = [
            {id: 1, title: 'Note9'},
            {id: 2, title: 'Note8'},
            {id: 3, title: 'Чехол для Note9'},
        ]
        storages = [ # склады
            {id: 1, title: 'Москва'},
            {id: 2, title: 'SPB'},
        ]
        stocks = [ # после инвенторизации на остатках
            {storage_id: 1, product_id: 1, quantity: 32},
            {storage_id: 1, product_id: 2, quantity: 14},
            {storage_id: 2, product_id: 1, quantity: 5},
        ]
        purchases = [ # закупленно
            {product_id: 1, quantity: 10, price: 90000},
            {product_id: 2, quantity: 10, price: 70000},
            {product_id: 3, quantity: 20, price: 300},
        ]
        sales = [ # проданно
            {product_id: 1, quantity: 3, price: 100000},
            {product_id: 2, quantity: 4, price: 90000},
            {product_id: 3, quantity: 1, price: 5000},
            {product_id: 3, quantity: 1, price: 1000}, # продали чехол по акции с телефоном 101000.
        ]

        Если город не указан, то какие офферы мы должны предлагать пользователю?


        Выход : нужна страница "продукта" на которой будет.
        Инфо о товре.
        Отзывы пользователей.

        Несколько офферов для город - который пользователь выбрал как основной:
        1) цена если только продукт купить
        2) цена старая если только одни прукт купить
        3) цена + расрочка = сколько платить в день
        4) цена со скидкой 3000 - добавить на точке услугу или акссесуар до 5000 рублей
        5) скидка 2% приоплате онлайн телефонов, 3% при оплате онлайн бытовой техники

        Сроки доставки - для города который пользователь выбрал как основной:
        1) Точки самовывоза и сроки когда на них можно забрать конкретный продукт.
        2) Зона курьерской доставки для города.
        3) Наличие доставки почтой россии для города.

        Возможное количество товара которое модно забрать на каждой из точек сомовывоза.


        Вопросы :
        1) Как форируется цена продукт в городе? От каких параметров зависит? Сколькими способами можем сформировать?
            1.1 Пусть цена в городе на продукт не завист от города но зависит от цены закупики данного продукта * 105 %.
                Цена закупки будет отличасть от партии к партии и от склада на которм находится товар.
            1.2 Жестко задали что цена в городе будет 15000.
            1.3 Задали что цена в городе зависеть от цены закупки + 1000 рублей.
        2) Как формируется прошлая цена?
        3) Рассрочка как формируется на товар?
        4) цена со скидкой 3000 - оффер содердит две позиции одна на 100000, друга на 5000, но суммарно 101000.
        5) Оффер стостоит из продукта и оплаты.


        P.S.
            В дальнейшем расмотреть еще 2 момента: курьерская доставка, отправка почтой россии.
        """
        pass

    def test_seller(self):
        city_moscow = City(title=u"Moscow")
        city_moscow.save()
        city_spb = City(title=u"SPB")
        city_spb.save()

        storage_1 = Storage(title=u"main storage")
        storage_1.save()

        pickup_point_1 = PickupPoint(title=u"pickup 1", city=city_moscow)
        pickup_point_1.save()
        pickup_point_2 = PickupPoint(title=u"pickup 2", city=city_moscow)
        pickup_point_2.save()
        pickup_point_3 = PickupPoint(title=u"pickup 3", city=city_spb)
        pickup_point_3.save()

        shop_1 = Shop(title=u"main shop")
        shop_1.save()
        shop_2 = Shop(title=u"next shop")
        shop_2.save()

        shop_1.add_pickup(pickup_point_1)
        shop_1.add_pickup(pickup_point_2)
        shop_1.add_pickup(pickup_point_3)

        shop_1.add_storage(storage_1)

        user_vova = User(first_name=u"Vova")

        session = Session(user=user_vova, city=city_moscow)

        brand = Brand()
        brand.save()
        product = Product(brand=brand)
        product.save()

        stock_1 = Stock(product=product, quantity=10, storage=storage_1, purchase_cost=105.1, currency="RUR")
        stock_1.save()

	filter_produce_1 = FilterProductCrossIdCategoryBrand()
        filter_produce_1.save()
	filter_storage_1 = FilterStorageId()
        filter_storage_1.save()
	filter_pickup_point_1 = FilterPickupPointIdCity()
        filter_pickup_point_1.save()
	price_factory_part_purchase_cost_from_stock_1 = PriceFactoryPartPurchaseCostFromStock(precent=10)
        price_factory_part_purchase_cost_from_stock_1.save()
	price_factory_fix_1 = PriceFactoryFix(price=150)
        price_factory_fix_1.save()

	price_policy_1 = PricePolicy()
        price_policy_1.save()
	price_policy_1.filter_produce.add(filter_produce_1)
	price_policy_1.filter_storage.add(filter_storage_1)
	price_policy_1.filter_pickup_point.add(filter_pickup_point_1)
	price_policy_1.price_factory_part_purchase_cost_from_stock.add(price_factory_part_purchase_cost_from_stock_1)
        price_policy_1.price_factory_fix.add(price_factory_fix_1)

        client_city = city_moscow
        client_type = 'onliner'

        seller = Seller(shop=shop_1)
	seller.save()
	seller.price_policies.add(price_policy_1)
	#seller.price_policies.add(price_policy_2)

        prices = seller.generate_prices(product, client_city, client_type)
        self.assertEqual([Decimal('115.61'), 150], prices)


    #def test_list_shop_for_session(self):
    def test_list_shop_for_user_with_pickup_in_city(self):
        """
        Получить список разрешенных магазинов в определнном городе для пользователя.
        К примеру с обычными пользователями не будут работать оптовые магазины.
        А соответсвенно нет необходимости получать от них офферы.
        """
        city_moscow = City(title=u"Moscow")
        city_moscow.save()
        city_spb = City(title=u"SPB")
        city_spb.save()

        user_vova = User(first_name=u"Vova")

        session = Session(user=user_vova, city=city_moscow)

        pickup_1 = PickupPoint(title=u"pickup 1", city=city_moscow)
        pickup_1.save()
        pickup_2 = PickupPoint(title=u"pickup 2", city=city_moscow)
        pickup_2.save()
        pickup_3 = PickupPoint(title=u"pickup 3", city=city_spb)
        pickup_3.save()

        shop_1 = Shop(title=u"main shop")
        shop_1.save()
        shop_2 = Shop(title=u"next shop")
        shop_2.save()

        shop_1.add_pickup(pickup_1)
        shop_1.add_pickup(pickup_2)
        shop_1.add_pickup(pickup_3)
        shop_2.add_pickup(pickup_1)

        catalog_shops = CatalogShops(title=u"main catalog")
        catalog_shops.save()
        #catalog_shops.add_shop_for_user_with_pickup_in_city(shop_1, city_moscow)
        #catalog_shops.add_shop_for_user_with_pickup_in_city(shop_2, city_spb)
        catalog_shops.add_shop(shop_1)
        catalog_shops.add_shop(shop_2)

        #shops = catalog_shops.allow_shops_for_session(session)
        shops = catalog_shops.allow_shops_for_user_with_pickup_in_city(user_vova, city_moscow)
        self.assertEqual([shop_1, shop_2], shops)

        shops = catalog_shops.allow_shops_for_user_with_pickup_in_city(user_vova, city_spb)
        self.assertEqual([shop_1], shops)


    #def test_list_offer_from_shop_for_session(self):
    def test_list_offer_from_shop_for_user_with_pickup_in_city(self):
        """
        Получить список офферов которые он может забрать в городе у выбранного магазина для пользователя.
        Айфоны в рознице, по причине политической, не продаем во всех городах Крыма .
        """
        city_moscow = City(title=u"Moscow")
        city_moscow.save()
        city_spb = City(title=u"SPB")
        city_spb.save()

        storage_1 = Storage(title=u"main storage")
        storage_1.save()

        pickup_point_1 = PickupPoint(title=u"pickup 1", city=city_moscow)
        pickup_point_1.save()
        pickup_point_2 = PickupPoint(title=u"pickup 2", city=city_moscow)
        pickup_point_2.save()
        pickup_point_3 = PickupPoint(title=u"pickup 3", city=city_spb)
        pickup_point_3.save()

        shop_1 = Shop(title=u"main shop")
        shop_1.save()
        shop_2 = Shop(title=u"next shop")
        shop_2.save()

        shop_1.add_pickup(pickup_point_1)
        shop_1.add_pickup(pickup_point_2)
        shop_1.add_pickup(pickup_point_3)

        user_vova = User(first_name=u"Vova")

        session = Session(user=user_vova, city=city_moscow)

        brand = Brand()
        brand.save()
        product = Product(brand=brand)
        product.save()

        #shop = Shop(title=u"main shop")
        #shop.save()

        factory_offer_1 = RepositoryOfferProductPriceStoragePickuppoint(
            shop=shop_1,
            text=u"offer 1 price 1 product 1 quantity 1 storage pickup_point",
            product=product,
            price=100000,
            #quantity=1,
            storage=storage_1,
            pickup_point=pickup_point_1, # конкретная точка получения
            #pickup_points=[pickup_point_1, pickup_point_2, pickup_point_3, ...] # множество точек получения
            #city_for_pickup=city_moscow, # город, для которого нужно взять все точки получения
            #filter_pickup_points=... # както сформированное множество точек получения 
            )
        factory_offer_1.save()
        factory_offer_2 = RepositoryOfferProductPriceStoragePickuppoint(
            shop=shop_1,
            text=u"offer 2 price 2 product 2 quantity 2 storage pickup_point",
            product=product,
            price=100000,
            storage=storage_1,
            pickup_point=pickup_point_1,
            )
        factory_offer_2.save()

        #shop.add_offer_for_user_with_pickup_in_city(offer_1, city_moscow)
        #shop.add_offer_for_user_with_pickup_in_city(offer_2, city_spb)

        #offers = shop.list_offer(session)
        offers = shop_1.list_offer_for_user_with_pickup_in_city(user_vova, city_moscow)
        self.assertEqual([factory_offer_1, factory_offer_2], offers)

        order = Order()

        shop_1.add_storage(storage_1)
        list_storage = shop_1.test_list_storage_for_user_with_pickup_in_city_with_order(user_vova, city_moscow, order)
        self.assertEqual([storage_1], list_storage)

        shop_1.add_pickup(pickup_point_1)
        list_pickup_point = shop_1.list_pickup_for_user_with_pickup_in_city_with_order(user_vova, city_moscow, order)
#        self.assertEqual([pickup_point_1], list_pickup_point)

