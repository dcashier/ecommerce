#!-*-coding: utf-8 -*-
from django.test import TestCase

from eshop.models import *
from django.test.client import Client
import json
import sys
import time
import pprint

# Create your tests here.

class TestEShop(TestCase):
    def setUp(self):
        print "SETUP DATA FOR ..."
        self.assertEqual.__self__.maxDiff = None

        #catalog_shops = CatalogShops(title=u"main catalog")
        #catalog_shops.save()

    #def test_list_shop_for_session(self):
    def test_list_shop_for_user_with_pickup_in_city(self):
        city_moscow = City(title=u"Moscow")
        city_spb = City(title=u"SPB")

        user_vova = User(first_name=u"Vova")

        session = Session(user=user_vova, city=city_moscow)

        shop_1 = Shop(title=u"main shop")
        shop_1.save()
        shop_2 = Shop(title=u"next shop")
        shop_2.save()

        catalog_shops = CatalogShops(title=u"main catalog")
        catalog_shops.save()
        catalog_shops.add_shop_for_user_with_pickup_in_city(shop_1, city_moscow)
        catalog_shops.add_shop_for_user_with_pickup_in_city(shop_2, city_spb)

        #shops = catalog_shops.allow_shops_for_session(session)
        shops = catalog_shops.allow_shops_for_user_with_pickup_in_city(user_vova, city_moscow)
        self.assertEqual([shop_1, shop_2], shops)

    #def test_list_offer_from_shop_for_session(self):
    def test_list_offer_from_shop_for_user_with_pickup_in_city(self):
        city_moscow = City(title=u"Moscow")
        city_spb = City(title=u"SPB")

        user_vova = User(first_name=u"Vova")

        session = Session(user=user_vova, city=city_moscow)

        offer_1 = Offer(text=u"offer 1 price 1 product 1 quantity 1")
        offer_1.save()
        offer_2 = Offer(text=u"offer 2 price 2 product 2 quantity 2")
        offer_2.save()

        shop = Shop(title=u"main shop")
        shop.save()
        shop.add_offer_for_user_with_pickup_in_city(offer_1, city_moscow)
        shop.add_offer_for_user_with_pickup_in_city(offer_2, city_spb)

        #offers = shop.list_offer(session)
        offers = shop.list_offer_for_user_with_pickup_in_city(user_vova, city_moscow)
        self.assertEqual([offer_1, offer_2], offers)

    #def test_list_storage_from_shop_for_session_with_order(self):
    def test_list_storage_from_shop_for_user_with_pickup_in_city_with_order(self):
        city_moscow = City(title=u"Moscow")
        city_spb = City(title=u"SPB")

        user_vova = User(first_name=u"Vova")

        session = Session(user=user_vova, city=city_moscow)

        storage_1 = Storage(title=u"main storage")
        storage_1.save()
        storage_2 = Storage(title=u"storage 2")
        storage_2.save()

        shop = Shop(title=u"main shop")
        shop.save()
        shop.add_storage(storage_1)

        offer_1 = Offer(text=u"offer 1 price 1 product 1 quantity 1")
        offer_2 = Offer(text=u"offer 2 price 2 product 2 quantity 2")
        order = Order()
        order.add_offer(offer_1)
        order.add_offer(offer_2)
        list_storage = shop.list_storage_for_user_with_pickup_in_city_with_order(user_vova, city_moscow, order)
        self.assertEqual([storage_1], list_storage)

    #def test_list_pickup_from_shop_for_session_with_order(self):
    def test_list_pickup_from_shop_for_user_with_pickup_in_city_with_order(self):
        city_moscow = City(title=u"Moscow")
        city_spb = City(title=u"SPB")

        user_vova = User(first_name=u"Vova")

        session = Session(user=user_vova, city=city_moscow)

        pickup_1 = Pickup(title=u"pickup 1")
        pickup_1.save()
        pickup_2 = Pickup(title=u"pickup 2")
        pickup_2.save()

        shop = Shop(title=u"main shop")
        shop.save()
        shop.add_pickup_for_user_with_pickup_in_city(pickup_1, city_moscow)

        offer_1 = Offer(text=u"offer 1 price 1 product 1 quantity 1")
        offer_2 = Offer(text=u"offer 2 price 2 product 2 quantity 2")
        order = Order()
        order.add_offer(offer_1)
        order.add_offer(offer_2)
        #list_pickup = shop.list_pickup(session, order)
        list_pickup = shop.list_pickup_for_user_with_pickup_in_city_with_order(user_vova, city_moscow, order)
        self.assertEqual([pickup_1], list_pickup)







        #customer_record = Entity(title=u"Клиет с улицы")
        #customer_record.save()

        #executor_record = Entity(title=u"Магазин - И.П.")
        #executor_record.save()

        #storage_record_1 = Storage(
        #    title=u"Склад 1",
        #    owner=executor_record
        #)
        #storage_record_1.save()

        #product_record_1 = Product(title=u"pr - 1")
        #product_record_1.save()

        #offer_record_1 = OfferRecord(
        #    storage_depart=storage_record_1,
        #    product=product_record_1,
        #    quantity=1,
        #    price=1100,
        #    datetime_ready_for_deaprt='2018-10-10 20:20:00',
        #    )
