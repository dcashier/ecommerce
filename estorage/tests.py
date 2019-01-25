#!-*-coding: utf-8 -*-
from django.test import TestCase

from estorage.models import *
from django.test.client import Client
import json
import sys
import time
import pprint
from decimal import Decimal

class TestEStorage(TestCase):
    def setUp(self):
        print "SETUP DATA FOR ..."
        self.assertEqual.__self__.maxDiff = None

    def test_seller(self):
        storage_1 = Storage(title=u"main storage")
        storage_1.save()

        brand_xiaomy = Brand(title="Xiaomy")
        brand_xiaomy.save()
        product_mi8 = Product(brand=brand_xiaomy)
        product_mi8.save()

        # Закупка пратии Mi8
        quantity_mi8 = 10
        purchase_cost_mi8 = 105.1
        currency_mi8 = "USD"
        part_number_1 = PartNumber()
        part_number_1.save()
        storage_1.load(product_mi8, quantity_mi8, part_number_1)
        quantity = storage_1.quantity(product_mi8)
        self.assertEqual(10, quantity)
        # закупка прошла успешно

        # Через несколько дней планируя высокий обем спроса на Ми8, закупили еще Mi8 но по чуть большей цене
        quantity_mi8_2 = 20
        purchase_cost_mi8_2 = 120
        currency_mi8_2 = "USD"
        part_number_2 = PartNumber()
        part_number_2.save()
        storage_1.load(product_mi8, quantity_mi8_2, part_number_2)
        quantity = storage_1.quantity(product_mi8)
        # с учетом предыдущих 10 ми8 суммарно получили 30
        self.assertEqual(30, quantity)
        # закупка прошла успешно
