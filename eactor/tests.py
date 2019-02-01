#!-*-coding: utf-8 -*-
from django.test import TestCase

from eactor.models import *
from django.test.client import Client
import json
import sys
import time
import pprint
from decimal import Decimal
import datetime

class TestEActor(TestCase):
    def setUp(self):
        print "SETUP DATA FOR ..."
        self.assertEqual.__self__.maxDiff = None

    def test_login(self):
        """
        Login
        """
        auth_system = AuthSystem()

        phone_number_1 = '+79161111111'
        password_1 = '11111'

        actor_1 = Actor(phone_number=phone_number_1, is_person=True)
        actor_1.save()
        actor_1.set_password(password_1)

        self.assertTrue(auth_system.has_actor_by_phone_numnber_password(phone_number_1, password_1))
        self.assertEqual(actor_1, auth_system.get_actor_by_phone_numnber_password(phone_number_1, password_1))

        phone_number_2 = '+79165432112'
        password_2 = '12345'

        actor_2 = Actor(phone_number=phone_number_2, is_person=True)
        actor_2.save()
        actor_2.set_password(password_2)

        self.assertTrue(auth_system.has_actor_by_phone_numnber_password(phone_number_2, password_2))
        self.assertEqual(actor_2, auth_system.get_actor_by_phone_numnber_password(phone_number_2, password_2))



        pass

#    def test_seller(self):
#        region_center = Region(title=u"Центральный")
#        region_center.save()
#        city_moscow = City(title=u"Moscow", region=region_center)
#        city_moscow.save()
#        city_spb = City(title=u"SPB", region=region_center)
#        city_spb.save()
#
#        storage_1 = Storage(title=u"main storage")
#        storage_1.save()
#
#        pickup_point_1 = PickupPoint(title=u"pickup 1", city=city_moscow)
#        pickup_point_1.save()
#        pickup_point_2 = PickupPoint(title=u"pickup 2", city=city_moscow)
#        pickup_point_2.save()
#        pickup_point_3 = PickupPoint(title=u"pickup 3", city=city_spb)
#        pickup_point_3.save()
#
#        shop_1 = Shop(title=u"main shop")
#        shop_1.save()
#        shop_2 = Shop(title=u"next shop")
#        shop_2.save()
#
#        shop_1.pickup_points.add(pickup_point_1)
#        shop_1.pickup_points.add(pickup_point_2)
#        shop_1.pickup_points.add(pickup_point_3)
#
#        shop_1.storages.add(storage_1)
#
#        brand_xiaomy = Brand(title="Xiaomy")
#        brand_xiaomy.save()
#        product_mi8 = Product(title='Mi 8', brand=brand_xiaomy)
#        product_mi8.save()
#
#        system_purchase = SystemPurchase()
#        system_purchase.save()
#
#        seller = Seller(shop=shop_1)
#	seller.save()
#
#        # Закупка пратии Mi8
#        #stock_1 = Stock(product=product_mi8, quantity=10, storage=storage_1, purchase_cost=105.1, currency="RUR")
#        #stock_1.save()
#        quantity_mi8 = 10
#        purchase_cost_mi8 = Decimal('105.1')
#        currency_mi8 = "USD"
#        part_number_1 = PartNumber()
#        part_number_1.save()
#        element_purchase = ElemetPurchase(system_purchase=system_purchase, quantity=quantity_mi8, product=product_mi8, part_number=part_number_1, purchase_cost=purchase_cost_mi8, purchase_currency=currency_mi8)
#        element_purchase.save()
#        #storage_1.load(product_mi8, quantity_mi8, purchase_cost_mi8, currency_mi8)
#        storage_1.load(product_mi8, quantity_mi8, part_number_1)
#        quantity = seller.quantity_for_sale(product_mi8)
#        self.assertEqual(10, quantity)
#        # закупка прошла успешно
#
#        # Через несколько дней планируя высокий обем спроса на Ми8, закупили еще Mi8 но по чуть большей цене
#        quantity_mi8_2 = 20
#        purchase_cost_mi8_2 = Decimal('120')
#        currency_mi8_2 = "USD"
#        part_number_2 = PartNumber()
#        part_number_2.save()
#        system_purchase = SystemPurchase()
#        system_purchase.save()
#        element_purchase = ElemetPurchase(system_purchase=system_purchase, quantity=quantity_mi8_2, product=product_mi8, part_number=part_number_2, purchase_cost=purchase_cost_mi8_2, purchase_currency=currency_mi8_2)
#        element_purchase.save()
#        storage_1.load(product_mi8, quantity_mi8_2, part_number_2)
#        quantity = seller.quantity_for_sale(product_mi8)
#        # с учетом предыдущих 10 ми8 суммарно получили 30
#        self.assertEqual(30, quantity)
#        # закупка прошла успешно
#
#        info_text = u"продавца попросили зарезервирвать для большиз босов"
#        reserve_for_big_boss_quantity = 2
#        #seller.reserve_product_on_storage(product_mi8, reserve_for_big_boss_quantity, storage_1, info_text)
#        seller.reserve_product_on_storage(product_mi8, reserve_for_big_boss_quantity, storage_1, info_text, part_number_1)
#        quantity = seller.quantity_for_sale(product_mi8)
#        self.assertEqual(28, quantity)
#        # Зарезервировали
#
#	filter_produce_1 = FilterProductCrossIdCategoryBrand()
#        filter_produce_1.save()
#        filter_produce_1.products.add(product_mi8)
#	filter_storage_1 = FilterStorageId()
#        filter_storage_1.save()
#	filter_pickup_point_1 = FilterPickupPointIdCity()
#        filter_pickup_point_1.save()
#	#price_factory_part_purchase_cost_from_stock_1 = PriceFactoryPartPurchaseCostFromStock(precent=10)
#        #price_factory_part_purchase_cost_from_stock_1.save()
#	price_factory_part_purchase_cost_1 = PriceFactoryPartPurchaseCost(precent=10)
#        price_factory_part_purchase_cost_1.save()
#	price_factory_fix_1 = PriceFactoryFix(price=150)
#        price_factory_fix_1.save()
#
#	price_policy_1 = PricePolicy()
#        price_policy_1.save()
#	price_policy_1.filter_produce.add(filter_produce_1)
#	price_policy_1.filter_storage.add(filter_storage_1)
#	price_policy_1.filter_pickup_point.add(filter_pickup_point_1)
#	#price_policy_1.price_factory_part_purchase_cost_from_stock.add(price_factory_part_purchase_cost_from_stock_1)
#	price_policy_1.price_factory_part_purchase_cost.add(price_factory_part_purchase_cost_1)
#        price_policy_1.price_factory_fix.add(price_factory_fix_1)
#
#	seller.price_policies.add(price_policy_1)
#	#seller.price_policies.add(price_policy_2)
#
#        client_city = city_moscow
#        client_type = 'onliner'
#
#        #Какие модели телефонов есть в вашем магазине на остатках?
#        products = seller.list_product_in_stock(category="mobile phone")
#        self.assertEqual([product_mi8], products)
#
#        # Так как для покупателей из разных городов матрицы у нас разные
#        # и зависят от многих праметров: 
#        #     политичекских - аппле в крыму не проддаем, 
#        #     на сахалине КБТ так как море не спокойно а воздухом возим только телефоны
#        products_allow = seller.list_allow_product_for_client(products, client_city, client_type)
#        self.assertEqual([product_mi8], products_allow)
#
#        # Из всего списка Вове понравился только Mi8
#        # Вова спрашивает у продавца какая цна на Mi8, если он придет на одну из Московских точек самовывоза?
#        prices = seller.prices(product_mi8, client_city, client_type)
#        self.assertEqual([Decimal('115.61'), Decimal('132.00'), 150], prices)
#
#        # а много у вас осталось Mi8 сейчас?
#        quantity = seller.quantity_for_sale(product_mi8)
#        self.assertEqual(28, quantity)
#
#        #Предлодить вове места ддля получнеия телефона
#        params_basket = [
#            {
#                'product': product_mi8,
#                'quantity': 1,
#                'price': Decimal('115.61'),
#                'currency': "USD",
#            },
#        ]
#        pickup_points = seller.pickup_points(params_basket, client_city, client_type)
#        self.assertEqual([pickup_point_1, pickup_point_2], pickup_points)
#
#        #Вова решил купить Ми8 за цену 115.61, оформляет заказ.
#        interval = [datetime.datetime(2000, 01, 01, 12, 30, 00), datetime.datetime(2000, 01, 01, 20, 00, 00)]
#        order_params = {
#            'version': 'v1',
#            'basket': [
#                {
#                    'product': product_mi8,
#                    'quantity': 1,
#                    'price': Decimal('115.61'),
#                    'currency': "USD",
#                },
#            ],
#            'pickup': {
#                'point': pickup_point_1,
#                'interval': interval,
#            },
#            'seller': None,
#            'client': None,
#        }
#        self.assertTrue(seller.is_allow_order(order_params))
#
#        # Потом Вова подмал и решил купить Ми8 вместе с чехлом Noname производителя по акции.
#        brand_noname = Brand(title="Noname")
#        brand_noname.save()
#        product_case_noname = Product(title="Case simple", brand=brand_noname)
#        product_case_noname.save()
#
#        order_params = {
#            'version': 'v1',
#            'basket': [
#                {
#                    'product': product_mi8,
#                    'quantity': 1,
#                    'price': Decimal('132.00'),
#                    'currency': "USD",
#                },
#                {
#                    'product': product_case_noname,
#                    'quantity': 1,
#                    'price': Decimal('10.00'),
#                    'currency': "USD",
#                },
#            ],
#            'pickup': {
#                'point': pickup_point_1,
#                'interval': interval,
#            },
#            'seller': None,
#            'client': None,
#        }
#        # Но мы еще не приняли на доступные склады нужное количество чехлов
#        #TODO проверить возращаемы ощибки
#        self.assertFalse(seller.is_allow_order(order_params))
#
#        quantity = seller.quantity_for_sale(product_case_noname)
#        self.assertEqual(0, quantity)
#
#        # Закупка пратии чехлов нонейм
#        system_purchase_3 = SystemPurchase()
#        system_purchase_3.save()
#
#        quantity_case_noname = 1000
#        purchase_cost_case_noname = Decimal('5.00')
#        currency_case_noname = "USD"
#        part_number_3 = PartNumber()
#        part_number_3.save()
#        element_purchase_3 = ElemetPurchase(system_purchase=system_purchase_3, quantity=quantity_case_noname, product=product_case_noname, part_number=part_number_3, purchase_cost=purchase_cost_case_noname, purchase_currency=currency_case_noname)
#        element_purchase_3.save()
#        storage_1.load(product_case_noname, quantity_case_noname, part_number_3)
#        quantity = seller.quantity_for_sale(product_case_noname)
#        self.assertEqual(1000, quantity)
#        # закупка прошла успешно
#
#        # Но мы еще не создали правило для продажи чехлов
#        self.assertFalse(seller.is_allow_order(order_params))
#
#        prices = seller.prices(product_case_noname, client_city, client_type)
#        self.assertEqual([], prices)
#
#        # Создаем правило для продажи чехлов
#	filter_produce_2 = FilterProductCrossIdCategoryBrand()
#        filter_produce_2.save()
#        filter_produce_2.brands.add(brand_noname)
#
#	price_factory_part_purchase_cost_2 = PriceFactoryPartPurchaseCost(precent=100)
#        price_factory_part_purchase_cost_2.save()
#
#	price_policy_2 = PricePolicy()
#        price_policy_2.save()
#	price_policy_2.filter_produce.add(filter_produce_2)
#	price_policy_2.price_factory_part_purchase_cost.add(price_factory_part_purchase_cost_2)
#
#	seller.price_policies.add(price_policy_2)
#
#        prices = seller.prices(product_case_noname, client_city, client_type)
#        self.assertEqual([Decimal('10.00')], prices)
#        # Правило отработало и вернуло допустимую цену
#
#        # Теперь заказа с такими параметрами создать возможно
#        self.assertTrue(seller.is_allow_order(order_params))
#
#        #Когда он выберет метсто рассчитать дату и время когда он то сможет забрать
#        #если все устраивает и пришла оплата, резериватьвать товар и перемещать на пункт выдачи
#        #когда вова за ним придет выдать товар офрмить чек, и начислить балы в системе лояльности.
#
##    def test_list_shop_for_user_with_pickup_in_city(self):
##        """
##        Получить список разрешенных магазинов в определнном городе для пользователя.
##        К примеру с обычными пользователями не будут работать оптовые магазины.
##        А соответсвенно нет необходимости получать от них офферы.
##        """
#
##    def test_list_offer_from_shop_for_user_with_pickup_in_city(self):
##        """
##        Получить список офферов которые он может забрать в городе у выбранного магазина для пользователя.
##        Айфоны в рознице, по причине политической, не продаем во всех городах Крыма .
##        """
