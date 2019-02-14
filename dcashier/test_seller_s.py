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

from eshop.models import *
from eseller.models import *
from eactor.models import *
from eproduct.models import *
from estorage.models import *
from eloyalty.models import *


class TestESellerS(TestCase):
    def setUp(self):
        """
        --DoOwner2@yandex.ru s--
        """
        print "SETUP DATA FOR ..."
        self.assertEqual.__self__.maxDiff = None

        size = 's'
        title_of_shop = 'Shop ii'
        title_of_pickup_points = ('Pickup point ii 1', 'Pickup point ii 2', 'Pickup point ii 3')
        title_of_owner = 'Owner ii'
        title_of_sellers = ('Cassir ii 1', 'Cassir ii 2')
        logins = ('DoOwner2@yandex.ru', 'DoSeller21@yandex.ru', 'DoSeller22@yandex.ru')
        title_of_actors = ('Actor ii Main ii', 'Actor ii 1', 'Actor ii 2')
        password_of_actors = ('12345', '12345', '12345')
        #list_product = []
        title_of_loyalty = "Loyalty 1"; max_percent = 40; start_ball = 1000000; start_ball_available_day = 20000; reward_percent = 10; available_day = 90; is_need_auth = False

        shop = Shop.objects.create(title=title_of_shop, size=size)

        region, c = Region.objects.get_or_create()
        city, c = City.objects.get_or_create(region=region)

        pickup_point_1 = PickupPoint.objects.create(title=title_of_pickup_points[0], city=city)
        pickup_point_2 = PickupPoint.objects.create(title=title_of_pickup_points[1], city=city)
        pickup_point_3 = PickupPoint.objects.create(title=title_of_pickup_points[2], city=city)

        owner = Seller.objects.create(title=title_of_owner, shop=shop)
        owner.pickup_points.add(pickup_point_1)
        owner.pickup_points.add(pickup_point_2)
        owner.pickup_points.add(pickup_point_3)
        actor_1 = Actor.objects.create(seller=owner, phone_number=logins[0], title=title_of_actors[0])
        actor_1.set_password(password_of_actors[0])

        seller_1 = Seller.objects.create(title=title_of_sellers[0], shop=shop)
        seller_1.pickup_points.add(pickup_point_1)
        seller_1.pickup_points.add(pickup_point_2)
        actor_2 = Actor.objects.create(seller=seller_1, phone_number=logins[1], title=title_of_actors[1])
        actor_2.set_password(password_of_actors[1])

        seller_2 = Seller.objects.create(title=title_of_sellers[1], shop=shop)
        seller_2.pickup_points.add(pickup_point_3)
        actor_3 = Actor.objects.create(seller=seller_2, phone_number=logins[2], title=title_of_actors[2])
        actor_3.set_password(password_of_actors[2])

        brand, c = Brand.objects.get_or_create()
        product, c = Product.objects.get_or_create(brand=brand, title='For take payment')
        product, c = Product.objects.get_or_create(brand=brand, title='Grean Tea')
        product, c = Product.objects.get_or_create(brand=brand, title='Balck Tea')
        product, c = Product.objects.get_or_create(brand=brand, title='Coffee')
        product, c = Product.objects.get_or_create(brand=brand, title='Dishes')
        product, c = Product.objects.get_or_create(brand=brand, title='Puer')

        srl = ServiceRepositoryLoyalty()
        srl.list_loyalty_for_owner(owner, shop)
        srl.has_loyalty_for_owner(owner, shop)
        srl.create_loyalty(owner, shop, title_of_loyalty, max_percent, start_ball, start_ball_available_day, reward_percent, available_day, is_need_auth)
        loyalty = srl.list_loyalty_for_owner(owner, shop)[0]
        srl.has_loyalty_for_owner(owner, shop)

    def test_1(self):
        """
        Проведем проверку заведения сесионных переменных и нескольких операций
        /
        /authPage.html
        /selectShopPage.html
        /shopPage.html
        /newDealPage.html
        /sellerDealPage.html
        """

        #init
        login = 'DoOwner2@yandex.ru'
        login_seller_1 = 'DoSeller21@yandex.ru'
        login_seller_2 = 'DoSeller22@yandex.ru'
        #

        client = Client()

        response = client.get('/')
        self.assertEqual(200, response.status_code)
        #self.assertEqual(None, response.content)
        #print response.content

        response = client.get('/shopPage.html')
        self.assertEqual(200, response.status_code)
        client.get('/newDealPage.html')
        self.assertEqual(200, response.status_code)
        client.get('/sellerDealPage.html')
        self.assertEqual(200, response.status_code)

        response = client.get('/authPage.html')
        self.assertEqual(200, response.status_code)
        #response = client.post('/login/', {'authNameInput': 'DoOwner1@yandex.ru', 'authPasswordInput': '12345'}, follow=True)
        #print response.redirect_chain
        response = client.post('/login/', {'authNameInput': login, 'authPasswordInput': '12345'})
        self.assertEqual(302, response.status_code)

        response = client.get('/')
        self.assertEqual(200, response.status_code)

        response = client.get('/selectShopPage.html')
        self.assertEqual(200, response.status_code)
        self.assertEqual(list(PickupPoint.objects.filter(id__in=[1,2,3])), list(response.context['shops']))

        response = client.post('/selectShopPage.html', {'shop_id': 1})
        self.assertEqual(302, response.status_code)

        response = client.get('/shopPage.html')
        self.assertEqual(200, response.status_code)
        self.assertEqual(PickupPoint.objects.get(id=1), response.context['shop'])

        response = client.get('/sellerDealPage.html')
        self.assertEqual(200, response.status_code)
        self.assertEqual([], list(response.context['orders']))

        response = client.post('/shopPage.html', {'customerPhoneInput': '89165556677', 'dealSummInput': 1000})
        self.assertEqual(302, response.status_code)

        response = client.get('/sellerDealPage.html')
        self.assertEqual(200, response.status_code)
        order = Order.objects.get(id=1)
        self.assertEqual([order], list(response.context['orders']))
        self.assertEqual(1000, list(response.context['orders'])[0].calculate_price_without_loyalty_balls())
        self.assertEqual(1000, list(response.context['orders'])[0].calculate_price())

        response = client.get('/newDealPage.html')
        self.assertEqual(200, response.status_code)

        self.assertEqual(1000, response.context['order_sum'])
        self.assertEqual(Shop.objects.get(id=2), response.context['client'])
        self.assertEqual(0, response.context['all_ball'])
        self.assertEqual(0, response.context['max_ball_for_pay'])
        self.assertEqual(40, response.context['max_percent_in_loyalty'])
        self.assertEqual(1000, response.context['order_sum_with_ball'])
        self.assertEqual(list(Product.objects.filter(id__in=[2,3,4,5,6])), response.context['special_products'])
        self.assertEqual([], response.context['selected_products'])

        response = client.post('/newDealPage.html', {'action': 'set_product', 'products': [3,5]})
        self.assertEqual(302, response.status_code)

        response = client.get('/sellerDealPage.html')
        self.assertEqual(200, response.status_code)
        order = Order.objects.get(id=1)
        self.assertEqual([order], list(response.context['orders']))
        self.assertEqual(1000, list(response.context['orders'])[0].calculate_price_without_loyalty_balls())
        self.assertEqual(1000, list(response.context['orders'])[0].calculate_price())

        response = client.get('/newDealPage.html')
        self.assertEqual(200, response.status_code)
        self.assertEqual(1000, response.context['order_sum'])
        self.assertEqual(Shop.objects.get(id=2), response.context['client'])
        self.assertEqual(0, response.context['all_ball'])
        self.assertEqual(0, response.context['max_ball_for_pay'])
        self.assertEqual(40, response.context['max_percent_in_loyalty'])
        self.assertEqual(1000, response.context['order_sum_with_ball'])
        self.assertEqual(list(Product.objects.filter(id__in=[2,3,4,5,6])), response.context['special_products'])
        self.assertEqual(list(Product.objects.filter(id__in=[3,5])), response.context['selected_products'])

        response = client.post('/newDealPage.html', {'action': 'write_off'})
        self.assertEqual(200, response.status_code)

        response = client.get('/sellerDealPage.html')
        self.assertEqual(200, response.status_code)
        order = Order.objects.get(id=1)
        self.assertEqual([order], list(response.context['orders']))
        self.assertEqual(1000, list(response.context['orders'])[0].calculate_price_without_loyalty_balls())
        self.assertEqual(1000, list(response.context['orders'])[0].calculate_price())

        response = client.get('/newDealPage.html')
        self.assertEqual(200, response.status_code)
        self.assertEqual(1000, response.context['order_sum'])
        self.assertEqual(Shop.objects.get(id=2), response.context['client'])
        self.assertEqual(100, response.context['all_ball'])
        self.assertEqual(100, response.context['max_ball_for_pay'])
        self.assertEqual(40, response.context['max_percent_in_loyalty'])
        self.assertEqual(900, response.context['order_sum_with_ball'])
        self.assertEqual(list(Product.objects.filter(id__in=[2,3,4,5,6])), response.context['special_products'])
        self.assertEqual(list(Product.objects.filter(id__in=[3,5])), response.context['selected_products'])


        # еще одна пкупка
        response = client.post('/shopPage.html', {'customerPhoneInput': '89165556677', 'dealSummInput': 20000})
        self.assertEqual(302, response.status_code)

        response = client.get('/newDealPage.html')
        self.assertEqual(200, response.status_code)
        self.assertEqual(20000, response.context['order_sum'])
        self.assertEqual(Shop.objects.get(id=2), response.context['client'])
        self.assertEqual(100, response.context['all_ball'])
        self.assertEqual(100, response.context['max_ball_for_pay'])
        self.assertEqual(40, response.context['max_percent_in_loyalty'])
        self.assertEqual(19900, response.context['order_sum_with_ball'])
        self.assertEqual(list(Product.objects.filter(id__in=[2,3,4,5,6])), response.context['special_products'])
        #self.assertEqual(list(Product.objects.filter(id__in=[3,5])), response.context['selected_products'])
        self.assertEqual([], response.context['selected_products'])

        response = client.post('/newDealPage.html', {'action': 'write_off'})
        #self.assertEqual(302, response.status_code)
        self.assertEqual(200, response.status_code)

        response = client.get('/newDealPage.html')
        self.assertEqual(200, response.status_code)
        self.assertEqual(20000, response.context['order_sum'])
        self.assertEqual(Shop.objects.get(id=2), response.context['client'])
        self.assertEqual(1990, response.context['all_ball'])
        self.assertEqual(1990, response.context['max_ball_for_pay'])
        self.assertEqual(40, response.context['max_percent_in_loyalty'])
        self.assertEqual(18010, response.context['order_sum_with_ball'])
        self.assertEqual(list(Product.objects.filter(id__in=[2,3,4,5,6])), response.context['special_products'])
        self.assertEqual([], response.context['selected_products'])


        # Теперь войдем под кассиром который имеет доступ ттолько к 2-м магазинам

        response = client.get('/')
        self.assertEqual(200, response.status_code)
        #self.assertEqual(None, response.content)
        #print response.content

        response = client.get('/shopPage.html')
        self.assertEqual(200, response.status_code)
        client.get('/newDealPage.html')
        self.assertEqual(200, response.status_code)
        client.get('/sellerDealPage.html')
        self.assertEqual(200, response.status_code)

        response = client.get('/authPage.html')
        self.assertEqual(200, response.status_code)
        #print response.redirect_chain
        response = client.post('/login/', {'authNameInput': login_seller_1, 'authPasswordInput': '12345'})
        self.assertEqual(302, response.status_code)

        response = client.get('/')
        self.assertEqual(200, response.status_code)

        response = client.get('/selectShopPage.html')
        self.assertEqual(200, response.status_code)
        self.assertEqual(list(PickupPoint.objects.filter(id__in=[1,2])), list(response.context['shops']))

        response = client.post('/selectShopPage.html', {'shop_id': 1})
        self.assertEqual(302, response.status_code)

        response = client.get('/shopPage.html')
        self.assertEqual(200, response.status_code)
        self.assertEqual(PickupPoint.objects.get(id=1), response.context['shop'])

        response = client.get('/sellerDealPage.html')
        self.assertEqual(200, response.status_code)
        self.assertEqual([], list(response.context['orders']))

        response = client.post('/shopPage.html', {'customerPhoneInput': '89165556677', 'dealSummInput': 1000})
        self.assertEqual(302, response.status_code)

        response = client.get('/sellerDealPage.html')
        self.assertEqual(200, response.status_code)
        order = Order.objects.get(id=3)
        self.assertEqual([order], list(response.context['orders']))
        self.assertEqual(1000, list(response.context['orders'])[0].calculate_price_without_loyalty_balls())
        self.assertEqual(1000, list(response.context['orders'])[0].calculate_price())

        response = client.get('/newDealPage.html')
        self.assertEqual(200, response.status_code)

        self.assertEqual(1000, response.context['order_sum'])
        self.assertEqual(Shop.objects.get(id=2), response.context['client'])
        self.assertEqual(1990, response.context['all_ball'])
        self.assertEqual(400, response.context['max_ball_for_pay'])
        self.assertEqual(40, response.context['max_percent_in_loyalty'])
        self.assertEqual(600, response.context['order_sum_with_ball'])
        self.assertEqual(list(Product.objects.filter(id__in=[2,3,4,5,6])), response.context['special_products'])
        self.assertEqual([], response.context['selected_products'])

        response = client.post('/newDealPage.html', {'action': 'set_product', 'products': [3,5]})
        self.assertEqual(302, response.status_code)

        response = client.get('/sellerDealPage.html')
        self.assertEqual(200, response.status_code)
        order = Order.objects.get(id=3)
        self.assertEqual([order], list(response.context['orders']))
        self.assertEqual(1000, list(response.context['orders'])[0].calculate_price_without_loyalty_balls())
        self.assertEqual(1000, list(response.context['orders'])[0].calculate_price())

        response = client.get('/newDealPage.html')
        self.assertEqual(200, response.status_code)
        self.assertEqual(1000, response.context['order_sum'])
        self.assertEqual(Shop.objects.get(id=2), response.context['client'])
        self.assertEqual(1990, response.context['all_ball'])
        self.assertEqual(400, response.context['max_ball_for_pay'])
        self.assertEqual(40, response.context['max_percent_in_loyalty'])
        self.assertEqual(600, response.context['order_sum_with_ball'])
        self.assertEqual(list(Product.objects.filter(id__in=[2,3,4,5,6])), response.context['special_products'])
        self.assertEqual(list(Product.objects.filter(id__in=[3,5])), response.context['selected_products'])

        response = client.post('/newDealPage.html', {'action': 'write_off'})
        self.assertEqual(200, response.status_code)

        response = client.get('/sellerDealPage.html')
        self.assertEqual(200, response.status_code)
        order = Order.objects.get(id=3)
        self.assertEqual([order], list(response.context['orders']))
        self.assertEqual(1000, list(response.context['orders'])[0].calculate_price_without_loyalty_balls())
        self.assertEqual(600, list(response.context['orders'])[0].calculate_price())

        response = client.get('/newDealPage.html')
        self.assertEqual(200, response.status_code)
        self.assertEqual(1000, response.context['order_sum'])
        self.assertEqual(Shop.objects.get(id=2), response.context['client'])
        self.assertEqual(1650, response.context['all_ball'])
        self.assertEqual(400, response.context['max_ball_for_pay'])
        self.assertEqual(40, response.context['max_percent_in_loyalty'])
        self.assertEqual(600, response.context['order_sum_with_ball'])
        self.assertEqual(list(Product.objects.filter(id__in=[2,3,4,5,6])), response.context['special_products'])
        self.assertEqual(list(Product.objects.filter(id__in=[3,5])), response.context['selected_products'])


        # еще одна пкупка
        response = client.post('/shopPage.html', {'customerPhoneInput': '89165556677', 'dealSummInput': 20000})
        self.assertEqual(302, response.status_code)

        response = client.get('/newDealPage.html')
        self.assertEqual(200, response.status_code)
        self.assertEqual(20000, response.context['order_sum'])
        self.assertEqual(Shop.objects.get(id=2), response.context['client'])
        self.assertEqual(1650, response.context['all_ball'])
        self.assertEqual(1650, response.context['max_ball_for_pay'])
        self.assertEqual(40, response.context['max_percent_in_loyalty'])
        self.assertEqual(18350, response.context['order_sum_with_ball'])
        self.assertEqual(list(Product.objects.filter(id__in=[2,3,4,5,6])), response.context['special_products'])
        self.assertEqual([], response.context['selected_products'])

        response = client.post('/newDealPage.html', {'action': 'write_off'})
        self.assertEqual(200, response.status_code)

        response = client.get('/newDealPage.html')
        self.assertEqual(200, response.status_code)
        self.assertEqual(20000, response.context['order_sum'])
        self.assertEqual(Shop.objects.get(id=2), response.context['client'])
        self.assertEqual(1835, response.context['all_ball'])
        self.assertEqual(1835, response.context['max_ball_for_pay'])
        self.assertEqual(40, response.context['max_percent_in_loyalty'])
        self.assertEqual(18165, response.context['order_sum_with_ball'])
        self.assertEqual(list(Product.objects.filter(id__in=[2,3,4,5,6])), response.context['special_products'])
        self.assertEqual([], response.context['selected_products'])
