#!-*-coding: utf-8 -*-
from django.db import models
from eproduct.models import *
from epartnumber.models import *

class SystemPurchase(models.Model):
    pass

class ElemetPurchase(models.Model):
    system_purchase = models.ForeignKey(SystemPurchase)
    quantity = models.IntegerField(u"Количество")
    product = models.ForeignKey(Product)
    part_number = models.ForeignKey(PartNumber)
    purchase_cost = models.DecimalField(u"стоимость закупки одной штуки", decimal_places=2, max_digits=7)
    purchase_currency = models.CharField(u"Валюта", max_length=5)

