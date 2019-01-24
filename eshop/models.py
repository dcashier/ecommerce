#!-*-coding: utf-8 -*-
from django.db import models
from estorage.models import *

class Shop(models.Model):
    title = models.CharField(max_length=200)
    pickup_points = models.ManyToManyField(PickupPoint)
    storages = models.ManyToManyField(Storage)
