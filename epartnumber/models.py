#!-*-coding: utf-8 -*-
from django.db import models

class PartNumber(models.Model):
    """
    В рамках одной партии на один товар может быть только одна цена закупки.
    """
    pass

