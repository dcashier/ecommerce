#!-*-coding: utf-8 -*-
from django.db import models
from estorage.models import *

class Shop(models.Model):
    """
    Точка продажи товара поккупателю. Это может быть розничный магазин, сайт, телегрма бот.
        Вопрос когда на сайте пользователь выбирает город, то для Москвы будет один магазин для Питера другой, для все России третий, а для Всего мира четвертый:
            Независимо от этого по у продавцов будет своя настройка цен для клиентов в разных городах.
    Вопрос касса Продавец и Кассир как связаны? Так как касс в магазине может быть много то у них разные номера, и они должны быть привязаны к точке продажи.
        Но если товра продается чераз интернет магазин, как и кто прибивает чек? И вообще пробивают ли на точке получения?
    """
    # поставщик / получатель
    title = models.CharField(verbose_name=u'Название Ип / ооо / оао', max_length=254, null=True, blank=True)
    pickup_points = models.ManyToManyField(PickupPoint)
    storages = models.ManyToManyField(Storage)
    is_person = models.BooleanField(verbose_name=u'Персона или Юр. лицо', default=False)
    birthday = models.DateField(u'Дата рождения', null=True, blank=True)
    phone_number = models.CharField(verbose_name=u'Номер мобильного', max_length=128, null=True, blank=True)
    phone_m_type = models.CharField(verbose_name=u'Тип номера мобильного', max_length=128, null=True, blank=True)
    fio = models.CharField(verbose_name=u'Ф.И.О.', max_length=128, null=True, blank=True)


