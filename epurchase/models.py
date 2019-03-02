#!-*-coding: utf-8 -*-
from django.db import models
from eproduct.models import *
from epartnumber.models import *

class SystemPurchase(models.Model):
    pass

class ElemetPurchase(models.Model):
    system_purchase = models.ForeignKey(SystemPurchase, on_delete=models.CASCADE)
    quantity = models.IntegerField(u"Количество")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    part_number = models.ForeignKey(PartNumber, on_delete=models.CASCADE)
    purchase_cost = models.DecimalField(u"стоимость закупки одной штуки", decimal_places=2, max_digits=7)
    purchase_currency = models.CharField(u"Валюта", max_length=5)

