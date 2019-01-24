#!-*-coding: utf-8 -*-
from django.db import models
from eproduct.models import *
from epartnumber.models import *

class SystemSale(models.Model):
    pass

class ElementSale(models.Model):
    system_sale= models.ForeignKey(SystemSale)
    quantity = models.IntegerField(u"Количество")
    product = models.ForeignKey(Product)
    part_number = models.ForeignKey(PartNumber)
    sale_cost = models.DecimalField(u"стоимость продажи одной штуки", decimal_places=2, max_digits=7)
    sale_currency = models.CharField(u"Валюта", max_length=5)


