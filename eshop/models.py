#!-*-coding: utf-8 -*-
from django.db import models
from estorage.models import *

class Shop(models.Model):
    # поставщик / получатель
    title = models.CharField(verbose_name=u'Название Ип / ооо / оао', max_length=254, null=True, blank=True)
    pickup_points = models.ManyToManyField(PickupPoint)
    storages = models.ManyToManyField(Storage)
    is_person = models.BooleanField(verbose_name=u'Персона или Юр. лицо', default=False)
    birthday = models.DateField(u'Дата рождения', null=True, blank=True)
    phone_number = models.CharField(verbose_name=u'Номер мобильного', max_length=128, null=True, blank=True)
    phone_m_type = models.CharField(verbose_name=u'Тип номера мобильного', max_length=128, null=True, blank=True)
    fio = models.CharField(verbose_name=u'Ф.И.О.', max_length=128, null=True, blank=True)


