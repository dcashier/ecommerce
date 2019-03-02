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
        print("SETUP DATA FOR ...")
        self.assertEqual.__self__.maxDiff = None

    def test_seller(self):
        storage_1 = Storage(title=u"main storage", size=10000)
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
        storage_1.push(product_mi8, quantity_mi8, part_number_1)
        quantity = storage_1.quantity(product_mi8)
        self.assertEqual(10, quantity)
        # закупка прошла успешно

        product_r = Product(brand=brand_xiaomy)
        product_r.save()

        # Закупка пратии r
        quantity_r = 5
        purchase_cost_r = 80
        currency_r = "USD"
        part_number_2 = PartNumber()
        part_number_2.save()
        storage_1.push(product_r, quantity_r, part_number_2)
        quantity = storage_1.quantity(product_r)
        self.assertEqual(5, quantity)
        # закупка прошла успешно

        self.assertEqual(15, storage_1.quantity_all())

        # Через несколько дней планируя высокий обем спроса на Ми8, закупили еще Mi8 но по чуть большей цене
        quantity_mi8_2 = 20
        purchase_cost_mi8_2 = 120
        currency_mi8_2 = "USD"
        part_number_2 = PartNumber()
        part_number_2.save()
        storage_1.push(product_mi8, quantity_mi8_2, part_number_2)
        quantity = storage_1.quantity(product_mi8)
        # с учетом предыдущих 10 ми8 суммарно получили 30
        self.assertEqual(30, quantity)
        # закупка прошла успешно

        self.assertEqual(35, storage_1.quantity_all())

        big_quantity = 1000
        # Выбрасывается исключение так как пытаемся списать товара больше чем есть вналичии
        self.assertRaises(AssertionError, storage_1.pull, product_mi8, big_quantity)

        storage_1.pull(product_mi8, 4)
        self.assertEqual(26, storage_1.quantity(product_mi8))

        self.assertEqual(31, storage_1.quantity_all())
