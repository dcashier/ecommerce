#!-*-coding: utf-8 -*-
from django.db import models
from eproduct.models import *
from estorage.models import *
from epartnumber.models import *

class Reserve(models.Model):
    """
    Для чего нужен резерв, чтобы данный товар не смоги продать другому агенту.
    Важно что приналичии 2-х и более складов товар должен остаться не задействованным только на оперделенном складе.
    Т.е. появляется понятие СВОБОДНЫЙ остаток.
    А также является ли система резервирования частью склада или нет?

    Надо поянть привзан ли резерв к остатку, и если привязан то:
        1. Каким образом они связаны?
        2. При перемещении остатков резер тоже должен перемещаться?
    Важно чтобы резервировался товар с опредененной ценой закупки? Да.
    """
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(u"Количество")
    storage = models.ForeignKey(Storage)
    part_number = models.ForeignKey(PartNumber)


