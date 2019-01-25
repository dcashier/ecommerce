#!-*-coding: utf-8 -*-
from django.test import TestCase

from esale.models import *
from django.test.client import Client
import json
import sys
import time
import pprint
from decimal import Decimal
import datetime

class TestESale(TestCase):
    def setUp(self):
        print "SETUP DATA FOR ..."
        self.assertEqual.__self__.maxDiff = None

    def test_seller(self):

        brand_xiaomy = Brand(title="Xiaomy")
        brand_xiaomy.save()
        product_mi8 = Product(brand=brand_xiaomy)
        product_mi8.save()

        brand_noname = Brand(title="Noname")
        brand_noname.save()
        product_case_noname = Product(brand=brand_noname)
        product_case_noname.save()

        region_center = Region(title=u"Центральный")
        region_center.save()
        city_moscow = City(title=u"Moscow", region=region_center)
        city_moscow.save()

        pickup_point_in_moscow = PickupPoint(title=u"pickup in moscow", city=city_moscow)
        pickup_point_in_moscow.save()

        interval = [datetime.datetime(2000, 01, 01, 12, 30, 00), datetime.datetime(2000, 01, 01, 20, 00, 00)]

        order_params = {
            'version': 'v1',
            'basket': [
                {
                    'product': product_mi8,
                    'quantity': 2,
                    'price': 150,
                    'currency': "USD",
                },
                {
                    'product': product_case_noname,
                    'quantity': 2,
                    'price': 5,
                    'currency': "USD",
                },
            ],
            'pickup': {
                'point': pickup_point_in_moscow,
                'interval': interval,
            },
            'seller': None,
            'client': None,
        }
        #self.assertTrue(Order.is_allow_order(order_params))
        #order = Order.create_order(order_params)

        storage_1 = Storage(title=u"main storage")
        storage_1.save()

        part_number_1 = PartNumber()
        part_number_1.save()
        #storage_1.load(product_mi8, quantity_mi8, part_number_1)
        #quantity = storage_1.quantity(product_mi8)
        #self.assertEqual(10, quantity)
        ## закупка прошла успешно

        ## Через несколько дней планируя высокий обем спроса на Ми8, закупили еще Mi8 но по чуть большей цене
        #quantity_mi8_2 = 20
        #purchase_cost_mi8_2 = 120
        #currency_mi8_2 = "USD"
        #part_number_2 = PartNumber()
        #part_number_2.save()
        #storage_1.load(product_mi8, quantity_mi8_2, part_number_2)
        #quantity = storage_1.quantity(product_mi8)
        ## с учетом предыдущих 10 ми8 суммарно получили 30
        #self.assertEqual(30, quantity)
        ## закупка прошла успешно
