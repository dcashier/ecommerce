#!-*-coding: utf-8 -*-
from django.test import TestCase

from eseller.models import *
from django.test.client import Client
import json
import sys
import time
import pprint
from decimal import Decimal
import datetime

class TestESeller(TestCase):
    def setUp(self):
        print "SETUP DATA FOR ..."
        self.assertEqual.__self__.maxDiff = None

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
        region_center = Region(title=u"Центральный")
        region_center.save()
        city_moscow = City(title=u"Moscow", region=region_center)
        city_moscow.save()
        city_spb = City(title=u"SPB", region=region_center)
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

        shop_1.pickup_points.add(pickup_point_1)
        shop_1.pickup_points.add(pickup_point_2)
        shop_1.pickup_points.add(pickup_point_3)

        shop_1.storages.add(storage_1)

        brand_xiaomy = Brand(title="Xiaomy")
        brand_xiaomy.save()
        product_mi8 = Product(title='Mi 8', brand=brand_xiaomy)
        product_mi8.save()

        system_purchase = SystemPurchase()
        system_purchase.save()

        seller = Seller(shop=shop_1)
	seller.save()

        # Закупка пратии Mi8
        #stock_1 = Stock(product=product_mi8, quantity=10, storage=storage_1, purchase_cost=105.1, currency="RUR")
        #stock_1.save()
        quantity_mi8 = 10
        purchase_cost_mi8 = Decimal('105.1')
        currency_mi8 = "USD"
        part_number_1 = PartNumber()
        part_number_1.save()
        element_purchase = ElemetPurchase(system_purchase=system_purchase, quantity=quantity_mi8, product=product_mi8, part_number=part_number_1, purchase_cost=purchase_cost_mi8, purchase_currency=currency_mi8)
        element_purchase.save()
        #storage_1.load(product_mi8, quantity_mi8, purchase_cost_mi8, currency_mi8)
        storage_1.load(product_mi8, quantity_mi8, part_number_1)
        quantity = seller.quantity_for_sale(product_mi8)
        self.assertEqual(10, quantity)
        # закупка прошла успешно

        # Через несколько дней планируя высокий обем спроса на Ми8, закупили еще Mi8 но по чуть большей цене
        quantity_mi8_2 = 20
        purchase_cost_mi8_2 = Decimal('120')
        currency_mi8_2 = "USD"
        part_number_2 = PartNumber()
        part_number_2.save()
        system_purchase = SystemPurchase()
        system_purchase.save()
        element_purchase = ElemetPurchase(system_purchase=system_purchase, quantity=quantity_mi8_2, product=product_mi8, part_number=part_number_2, purchase_cost=purchase_cost_mi8_2, purchase_currency=currency_mi8_2)
        element_purchase.save()
        storage_1.load(product_mi8, quantity_mi8_2, part_number_2)
        quantity = seller.quantity_for_sale(product_mi8)
        # с учетом предыдущих 10 ми8 суммарно получили 30
        self.assertEqual(30, quantity)
        # закупка прошла успешно

        info_text = u"продавца попросили зарезервирвать для большиз босов"
        reserve_for_big_boss_quantity = 2
        #seller.reserve_product_on_storage(product_mi8, reserve_for_big_boss_quantity, storage_1, info_text)
        seller.reserve_product_on_storage(product_mi8, reserve_for_big_boss_quantity, storage_1, info_text, part_number_1)
        quantity = seller.quantity_for_sale(product_mi8)
        self.assertEqual(28, quantity)
        # Зарезервировали

	filter_produce_1 = FilterProductCrossIdCategoryBrand()
        filter_produce_1.save()
        filter_produce_1.products.add(product_mi8)
	filter_storage_1 = FilterStorageId()
        filter_storage_1.save()
	filter_pickup_point_1 = FilterPickupPointIdCity()
        filter_pickup_point_1.save()
	#price_factory_part_purchase_cost_from_stock_1 = PriceFactoryPartPurchaseCostFromStock(precent=10)
        #price_factory_part_purchase_cost_from_stock_1.save()
	price_factory_part_purchase_cost_1 = PriceFactoryPartPurchaseCost(precent=10)
        price_factory_part_purchase_cost_1.save()
	price_factory_fix_1 = PriceFactoryFix(price=150)
        price_factory_fix_1.save()

	price_policy_1 = PricePolicy()
        price_policy_1.save()
	price_policy_1.filter_produce.add(filter_produce_1)
	price_policy_1.filter_storage.add(filter_storage_1)
	price_policy_1.filter_pickup_point.add(filter_pickup_point_1)
	#price_policy_1.price_factory_part_purchase_cost_from_stock.add(price_factory_part_purchase_cost_from_stock_1)
	price_policy_1.price_factory_part_purchase_cost.add(price_factory_part_purchase_cost_1)
        price_policy_1.price_factory_fix.add(price_factory_fix_1)

	seller.price_policies.add(price_policy_1)
	#seller.price_policies.add(price_policy_2)

        client_city = city_moscow
        client_type = 'onliner'

        #Какие модели телефонов есть в вашем магазине на остатках?
        products = seller.list_product_in_stock(category="mobile phone")
        self.assertEqual([product_mi8], products)

        # Так как для покупателей из разных городов матрицы у нас разные
        # и зависят от многих праметров: 
        #     политичекских - аппле в крыму не проддаем, 
        #     на сахалине КБТ так как море не спокойно а воздухом возим только телефоны
        products_allow = seller.list_allow_product_for_client(products, client_city, client_type)
        self.assertEqual([product_mi8], products_allow)

        # Из всего списка Вове понравился только Mi8
        # Вова спрашивает у продавца какая цна на Mi8, если он придет на одну из Московских точек самовывоза?
        prices = seller.prices(product_mi8, client_city, client_type)
        self.assertEqual([Decimal('115.61'), Decimal('132.00'), 150], prices)

        # а много у вас осталось Mi8 сейчас?
        quantity = seller.quantity_for_sale(product_mi8)
        self.assertEqual(28, quantity)

        #Предлодить вове места ддля получнеия телефона
        params_basket = [
            {
                'product': product_mi8,
                'quantity': 1,
                'price': Decimal('115.61'),
                'currency': "USD",
            },
        ]
        pickup_points = seller.pickup_points(params_basket, client_city, client_type)
        self.assertEqual([pickup_point_1, pickup_point_2], pickup_points)

        #Вова решил купить Ми8 за цену 115.61, оформляет заказ.
        interval = [datetime.datetime(2000, 01, 01, 12, 30, 00), datetime.datetime(2000, 01, 01, 20, 00, 00)]
        order_params = {
            'version': 'v1',
            'basket': [
                {
                    'product': product_mi8,
                    'quantity': 1,
                    'price': Decimal('115.61'),
                    'currency': "USD",
                },
            ],
            'pickup': {
                'point': pickup_point_1,
                'interval': interval,
            },
            'seller': None,
            'client': None,
        }
        self.assertTrue(seller.is_allow_order(order_params))

        # Потом Вова подмал и решил купить Ми8 вместе с чехлом Noname производителя по акции.
        brand_noname = Brand(title="Noname")
        brand_noname.save()
        product_case_noname = Product(title="Case simple", brand=brand_noname)
        product_case_noname.save()

        order_params = {
            'version': 'v1',
            'basket': [
                {
                    'product': product_mi8,
                    'quantity': 1,
                    'price': Decimal('132.00'),
                    'currency': "USD",
                },
                {
                    'product': product_case_noname,
                    'quantity': 1,
                    'price': Decimal('10.00'),
                    'currency': "USD",
                },
            ],
            'pickup': {
                'point': pickup_point_1,
                'interval': interval,
            },
            'seller': None,
            'client': None,
        }
        # Но мы еще не приняли на доступные склады нужное количество чехлов
        #TODO проверить возращаемы ощибки
        self.assertFalse(seller.is_allow_order(order_params))

        quantity = seller.quantity_for_sale(product_case_noname)
        self.assertEqual(0, quantity)

        # Закупка пратии чехлов нонейм
        system_purchase_3 = SystemPurchase()
        system_purchase_3.save()

        quantity_case_noname = 1000
        purchase_cost_case_noname = Decimal('5.00')
        currency_case_noname = "USD"
        part_number_3 = PartNumber()
        part_number_3.save()
        element_purchase_3 = ElemetPurchase(system_purchase=system_purchase_3, quantity=quantity_case_noname, product=product_case_noname, part_number=part_number_3, purchase_cost=purchase_cost_case_noname, purchase_currency=currency_case_noname)
        element_purchase_3.save()
        storage_1.load(product_case_noname, quantity_case_noname, part_number_3)
        quantity = seller.quantity_for_sale(product_case_noname)
        self.assertEqual(1000, quantity)
        # закупка прошла успешно

        # Но мы еще не создали правило для продажи чехлов
        self.assertFalse(seller.is_allow_order(order_params))

        prices = seller.prices(product_case_noname, client_city, client_type)
        self.assertEqual([], prices)

        # Создаем правило для продажи чехлов
	filter_produce_2 = FilterProductCrossIdCategoryBrand()
        filter_produce_2.save()
        filter_produce_2.brands.add(brand_noname)

	price_factory_part_purchase_cost_2 = PriceFactoryPartPurchaseCost(precent=100)
        price_factory_part_purchase_cost_2.save()

	price_policy_2 = PricePolicy()
        price_policy_2.save()
	price_policy_2.filter_produce.add(filter_produce_2)
	price_policy_2.price_factory_part_purchase_cost.add(price_factory_part_purchase_cost_2)

	seller.price_policies.add(price_policy_2)

        prices = seller.prices(product_case_noname, client_city, client_type)
        self.assertEqual([Decimal('10.00')], prices)
        # Правило отработало и вернуло допустимую цену

        # Теперь заказа с такими параметрами создать возможно
        self.assertTrue(seller.is_allow_order(order_params))

        #Когда он выберет метсто рассчитать дату и время когда он то сможет забрать
        #если все устраивает и пришла оплата, резериватьвать товар и перемещать на пункт выдачи
        #когда вова за ним придет выдать товар офрмить чек, и начислить балы в системе лояльности.

    def test_create_client(self):
        shop_1 = Shop(title=u"main shop")
        shop_1.save()

        seller_1 = Seller(shop=shop_1)
        seller_1.save()

        client_phone_number = '+71002003040'
        self.assertTrue(seller_1.is_work_in_shop(shop_1))
        self.assertFalse(seller_1.has_shop_client_with_phone_number(shop_1, client_phone_number))

        shop_2 = Shop(title=u"shop two")
        shop_2.save()

        seller_2_1 = Seller(shop=shop_2)
        seller_2_1.save()

        self.assertTrue(seller_2_1.is_work_in_shop(shop_2))
        self.assertFalse(seller_1.is_work_in_shop(shop_2))
        self.assertFalse(seller_2_1.is_work_in_shop(shop_1))
        try:
            seller_1.has_shop_client_with_phone_number(shop_2, client_phone_number)
        except:
            pass
        else:
            # Если появилось исключение значит права нарушены
            self.assertFalse(True)
        try:
            seller_1.create_client_shop_with_phone_number(shop_2, client_phone_number)
        except:
            pass
        else:
            # Если появилось исключение значит права нарушены
            self.assertFalse(True)
        self.assertFalse(seller_2_1.has_shop_client_with_phone_number(shop_2, client_phone_number))
        seller_2_1.create_client_shop_with_phone_number(shop_2, client_phone_number)

        client = seller_2_1.get_client_shop_with_phone_number(shop_2, client_phone_number)
        self.assertEqual(client_phone_number, client.get_phone_number())

        self.assertFalse(seller_1.has_shop_client_with_phone_number(shop_1, client_phone_number))
        self.assertTrue(seller_2_1.has_shop_client_with_phone_number(shop_2, client_phone_number))

        self.assertFalse(seller_1.has_shop_client(shop_1, client))
        self.assertTrue(seller_2_1.has_shop_client(shop_2, client))

        seller_2_2 = Seller(shop=shop_2)
        seller_2_2.save()

        self.assertFalse(seller_2_2.is_work_in_shop(shop_1))
        self.assertTrue(seller_2_2.is_work_in_shop(shop_2))
        self.assertTrue(seller_2_2.has_shop_client_with_phone_number(shop_2, client_phone_number))
        self.assertTrue(seller_2_2.has_shop_client(shop_2, client))
        self.assertEqual(client_phone_number, seller_2_2.get_client_shop_with_phone_number(shop_2, client_phone_number).get_phone_number())


#    def test_list_shop_for_user_with_pickup_in_city(self):
#        """
#        Получить список разрешенных магазинов в определнном городе для пользователя.
#        К примеру с обычными пользователями не будут работать оптовые магазины.
#        А соответсвенно нет необходимости получать от них офферы.
#        """

#    def test_list_offer_from_shop_for_user_with_pickup_in_city(self):
#        """
#        Получить список офферов которые он может забрать в городе у выбранного магазина для пользователя.
#        Айфоны в рознице, по причине политической, не продаем во всех городах Крыма .
#        """
