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


class TestESellerXS(TestCase):
    def setUp(self):
        """
        --DoOwner1@yandex.ru xs--
        """
        print "SETUP DATA FOR ..."
        self.assertEqual.__self__.maxDiff = None

        size = 'xs'
        title_of_shop = 'Shop 1'
        title_of_pickup_point = 'Pickup point 1'
        title_of_seller = 'Cassir 1'
        login = 'DoOwner1@yandex.ru'
        title_of_actor = 'Actor 1'
        password_of_actor = '12345'
        #list_product = []
        title_of_loyalty = "Loyalty 1";
        max_percent = 40;
        start_ball = 1000000;
        start_ball_available_day = 20000;
        reward_percent = 10;
        available_day = 90;
        is_need_auth = False

        region, c = Region.objects.get_or_create()
        city, c = City.objects.get_or_create(region=region)
        pickup_point, c = PickupPoint.objects.get_or_create(city=city, title=title_of_pickup_point)
        shop = Shop.objects.create(title=title_of_shop, size=size)
        seller = Seller.objects.create(title=title_of_seller, shop=shop)
        seller.pickup_points.add(pickup_point)
        actor = Actor.objects.create(seller=seller, phone_number=login, title=title_of_actor)
        actor.set_password(password_of_actor)
        brand, c = Brand.objects.get_or_create()
        product, c = Product.objects.get_or_create(brand=brand, title='For take payment')
        product, c = Product.objects.get_or_create(brand=brand, title='Grean Tea')
        product, c = Product.objects.get_or_create(brand=brand, title='Balck Tea')
        product, c = Product.objects.get_or_create(brand=brand, title='Coffee')
        product, c = Product.objects.get_or_create(brand=brand, title='Dishes')
        product, c = Product.objects.get_or_create(brand=brand, title='Puer')
        srl = ServiceRepositoryLoyalty()
        srl.list_loyalty_for_owner(seller, shop)
        srl.has_loyalty_for_owner(seller, shop)
        srl.create_loyalty(seller, shop, title_of_loyalty, max_percent, start_ball, start_ball_available_day, reward_percent, available_day, is_need_auth)
        loyalty = srl.list_loyalty_for_owner(seller, shop)[0]
        srl.has_loyalty_for_owner(seller, shop)

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
        login = 'DoOwner1@yandex.ru'

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

        # После внедрения процесинга и статусов этот кусок развалится
        #response = client.post('/newDealPage.html', {'action': 'save_up'})
        #self.assertEqual(200, response.status_code)
        #response = client.post('/newDealPage.html', {'action': 'save_up'})
        ##self.assertEqual(302, response.status_code)
        #self.assertEqual(200, response.status_code)
        #response = client.post('/newDealPage.html', {'action': 'save_up'})
        ##self.assertEqual(302, response.status_code)
        #self.assertEqual(200, response.status_code)
        #response = client.post('/newDealPage.html', {'action': 'save_up'})
        ##self.assertEqual(302, response.status_code)
        #self.assertEqual(200, response.status_code)
        #response = client.post('/newDealPage.html', {'action': 'save_up'})
        ##self.assertEqual(302, response.status_code)
        #self.assertEqual(200, response.status_code)
        #response = client.post('/newDealPage.html', {'action': 'save_up'})
        ##self.assertEqual(302, response.status_code)
        #self.assertEqual(200, response.status_code)

        #response = client.get('/sellerDealPage.html')
        #self.assertEqual(200, response.status_code)
        #order = Order.objects.get(id=1)
        #self.assertEqual([order], list(response.context['orders']))
        #self.assertEqual(1000, list(response.context['orders'])[0].calculate_price_without_loyalty_balls())
        #self.assertEqual(1000, list(response.context['orders'])[0].calculate_price())

        #response = client.get('/newDealPage.html')
        #self.assertEqual(200, response.status_code)
        #self.assertEqual(1000, response.context['order_sum'])
        #self.assertEqual(Shop.objects.get(id=2), response.context['client'])
        #self.assertEqual(100, response.context['all_ball'])
        #self.assertEqual(100, response.context['max_ball_for_pay'])
        #self.assertEqual(40, response.context['max_percent_in_loyalty'])
        #self.assertEqual(900, response.context['order_sum_with_ball'])
        #self.assertEqual(list(Product.objects.filter(id__in=[2,3,4,5,6])), response.context['special_products'])
        #self.assertEqual(list(Product.objects.filter(id__in=[3,5])), response.context['selected_products'])

        #response = client.post('/newDealPage.html', {'action': 'write_off'})
        ##self.assertEqual(302, response.status_code)
        #self.assertEqual(200, response.status_code)

        #response = client.get('/sellerDealPage.html')
        #self.assertEqual(200, response.status_code)
        #order = Order.objects.get(id=1)
        #self.assertEqual([order], list(response.context['orders']))
        #self.assertEqual(1000, list(response.context['orders'])[0].calculate_price_without_loyalty_balls())
        #self.assertEqual(600, list(response.context['orders'])[0].calculate_price())

        #response = client.get('/newDealPage.html')
        #self.assertEqual(200, response.status_code)
        #self.assertEqual(1000, response.context['order_sum'])
        #self.assertEqual(Shop.objects.get(id=2), response.context['client'])
        #self.assertEqual(360, response.context['all_ball'])
        #self.assertEqual(360, response.context['max_ball_for_pay'])
        #self.assertEqual(40, response.context['max_percent_in_loyalty'])
        #self.assertEqual(640, response.context['order_sum_with_ball'])
        #self.assertEqual(list(Product.objects.filter(id__in=[2,3,4,5,6])), response.context['special_products'])
        #self.assertEqual(list(Product.objects.filter(id__in=[3,5])), response.context['selected_products'])

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

