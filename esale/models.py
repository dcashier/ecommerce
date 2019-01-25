#!-*-coding: utf-8 -*-
from django.db import models
from eproduct.models import *
from epartnumber.models import *
from estorage.models import *

class Order(models.Model):
    """
    Можно учитывать как один из элементов отчетности по продажам. Возможно как отчет.
    Сокращенный:
    {
        cargo: [
            {
                product
                quantity
            },
            ...
        ]
        shop
        client
        price
    }

    Расширенный:
    {
        order: [
            {
                product_goods
                quantity
                price
                price_policy: [...]
                    акция на какую то часть заказа которая привела к изменнию цены
                        т.е. указать политику которая привела к формированию такой цены.
                            И срок рассчета цены на основе данной политики так как она могла поменяться к сегодняшнему моменту
                price_whitout_sale
                    цена "стандарнтная" на данный товар
                        надо потом понять и определить что занчит стандартная цена - цена на основе какой то стандартной политики
                        или цена которая действует на данный товар при покупке в размере одна штука опалатой наличными при наличии на данной точеке самовывоза
            },
            {
                product_service
                quantity
                price
                price_policy: [...]
                price_whitout_sale
            },
           ...
        ]
        [
            {
            },
            ...
        ]
        history_move: [
            {
                cargo: [
                    {
                        product_goods
                        quantity
                    },
                    ...
                ],
                depart: {
                    point
                    datetime
                },
                arrival: {
                    point
                    datetime
                },
                courier
            },
            {},
            ...
        ],
        pickup: [
            {
                order: [
                    {
                        product_goods
                        quantity
                    },
                    {
                        product_service
                        quantity
                    },
                    ...
                ]
                point
                datetime
                interval
            },
            ...
        ]
    }
    """
    client_title = models.CharField(u"Название клиента", max_length=128)
    create_datetime = models.DateTimeField(u'дата и время создание заказа')
    pickup_point = models.ForeignKey(PickupPoint)
    pickup_dateteme = models.DateTimeField(u'дата и время вручения всего заказа(т.е. последней партии)')

    def calculaet_cost(self):
        """
        Рассчитывает финальную стомость на основе всех рализуемых позиций.
            Можно позволить простое суммирование,
                так как налоговая требует точную сумму реализации по каждой позиции,
                а значит действие всех скидок и акций на ней отразится.
        """
        return 0

    def pickup_points(self):
        """
        Точка получения всегда одна в нашем текущем подходе, но возращаем спиок чтобы ...
        """
        return [self.pickup_point]

    def history_move_goods(self):
        """
        Перемещение между складами теребуется только для товаров(для услуг оно не требуется)
        """
        return []

class NotImportantInformation(models.Model):
    order = models.ForeignKey(Order)
    part_number = models.ForeignKey(PartNumber)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(u"Количество")

class ElementSale(models.Model):
    """
    Магазин
    Кассовый апарат
    Каcсир - тот кто на кассе(сайт продавший)
    Продавец - тот кто сформировал цену, озвучил сроки(так же может быть сайт или телеграм бот или ...)
    Возможно стоит указать склад с которго будет изьят данный торва
    Точку выдачи - где будет произведена выдача
    Дату получения товара

    В рамках заказа нужно:
        создать дукуменыт,
        напечать чеки,
        получить подтвержение оплаты из банка,
        осуществить внутренню логистику по перемещению всего требуемого на точку выдачи
            (не учитываем случай получения части заказа в разных метсах)

    """
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(u"Количество")
    sale_price = models.DecimalField(u"стоимость продажи одной штуки", decimal_places=2, max_digits=7)
    sale_currency = models.CharField(u"Валюта", max_length=5)


