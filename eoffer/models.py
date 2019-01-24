#!-*-coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from eproduct.models import *
from estorage.models import *
from epartnumber.models import *
from ereserve.models import *
from epricepolicy.models import *

# Фабрики офферов, офферы, фильтры офферов.

# Офферы могут быть разных типов, но им следует действовать в соответствии с одним интрефейсом
class Offer(object):
    def is_allow_for_pickup_point(self, pickup_point):
        return True

    def is_allow_for_pickup_city(self, pickup_city):
        return True

    def is_allow_for_storage(self, storage):
        return True

    def is_allow_for_seller(self, seller):
        return True

class FactoryOfferPrecentfrompurchasecost(models.Model, Offer):
    """
    Наценка на любой продукт : самый простой подход создаем наценку на в 10% от закупочной цены на все продукты.
    """
    text = models.CharField(max_length=200)
    precent_from_purchase_cost = models.IntegerField(u"Процент от цена закупки на указаном складе")
    shop = models.ForeignKey(Shop)

class FactoryOfferCategoriesPrecentfrompurchasecost(models.Model, Offer):
    """
    Наценка на любой продукт из списка категорий : самый простой подход создаем наценку на в 10% от закупочной цены на все продукты.
    """
    text = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
    precent_from_purchase_cost = models.IntegerField(u"Процент от цена закупки на указаном складе")
    shop = models.ForeignKey(Shop)

class RepositoryOfferProductPrice(models.Model, Offer):
    """
    самый простой цена и продукт
    """
    text = models.CharField(max_length=200)
    product = models.ForeignKey(Product)
    price = models.IntegerField(u"Цена")
    currency = models.CharField(u"Валюта", max_length=5)
    shop = models.ForeignKey(Shop)

class RepositoryOfferProductPriceQuantity(models.Model, Offer):
    """
    для отовиков, за единоверменную покупку 10 штук суммарно заплатите на 5% меньше.
    """
    text = models.CharField(max_length=200)
    product = models.ForeignKey(Product)
    price = models.IntegerField(u"Цена")
    currency = models.CharField(u"Валюта", max_length=5)
    quantity = models.IntegerField(u"Штук")
    shop = models.ForeignKey(Shop)

class RepositoryOfferProductPricePickupcity(models.Model, Offer):
    """
    если товар забирут в определнном городе. Так как на сахалине мало предложений то хотим продавать там дороже.
    """
    text = models.CharField(max_length=200)
    product = models.ForeignKey(Product)
    price = models.IntegerField(u"Цена")
    currency = models.CharField(u"Валюта", max_length=5)
    pickup_city = models.ForeignKey(City) # для всех точек pickup в этом городе
    shop = models.ForeignKey(Shop)

    def is_allow_for_pickup_point(self, pickup_point):
        if pickup_point.city == self.pickup_city:
            return True
        return False

    def is_allow_for_pickup_city(self, pickup_city):
        if pickup_city == self.pickup_city:
            return True
        return False

class RepositoryOfferProductPricePickuppoint(models.Model, Offer):
    """
    Хотим разрекламировать новый магазин и там слали специальные цены.
    """
    text = models.CharField(max_length=200)
    product = models.ForeignKey(Product)
    price = models.IntegerField(u"Цена")
    currency = models.CharField(u"Валюта", max_length=5)
    pickup_point = models.ForeignKey(PickupPoint) # для данной точки получения
    shop = models.ForeignKey(Shop)

    def is_allow_for_pickup_point(self, pickup_point):
        if pickup_point == self.pickup_point:
            return True
        return False

    def is_allow_for_pickup_city(self, pickup_city):
        if pickup_city == self.pickup_point.city:
            return True
        return False

class RepositoryOfferProductPriceStorage(models.Model, Offer):
    """
    если товар едет с этого склада то на него действет такая цена
    """
    text = models.CharField(max_length=200)
    product = models.ForeignKey(Product)
    price = models.IntegerField(u"Цена")
    currency = models.CharField(u"Валюта", max_length=5)
    storage = models.ForeignKey(Storage) # для всех точек pickup в этом городе
    shop = models.ForeignKey(Shop)

    def is_allow_for_storage(self, storage):
        if storage == self.storage:
            return True
        return False

class RepositoryOfferProductPriceStoragePickuppoint(models.Model, Offer):
    """
    Для точки получения в Москве если товар едет с московского склада цена одна, а если точка получения на Сахалинее и товар едет также с московского скалада то цена будет другой.
    """
    text = models.CharField(max_length=200)
    product = models.ForeignKey(Product)
    price = models.IntegerField(u"Цена")
    currency = models.CharField(u"Валюта", max_length=5)
    storage = models.ForeignKey(Storage) # для всех точек pickup в этом городе
    pickup_point = models.ForeignKey(PickupPoint) # для данной точки получения
    shop = models.ForeignKey(Shop)

    def is_allow_for_pickup_point(self, pickup_point):
        if pickup_point == self.pickup_point:
            return True
        return False

    def is_allow_for_pickup_city(self, pickup_city):
        if pickup_city == self.pickup_point.city:
            return True
        return False

    def is_allow_for_storage(self, storage):
        if storage == self.storage:
            return True
        return False

class RepositoryOfferProductPrecentfrompurchasecostStoragePickuppoint(models.Model, Offer):
    """
    Для точеки получения на Сахалинее, если товар едет с московского скалада то цена будет на 10% процентов выше по сравнению с ценой закупки(у товара на складе в этом случае должна быть цена закупки), а если точка получения в Москве то всего на 3%.
    """
    text = models.CharField(max_length=200)
    product = models.ForeignKey(Product)
    precent_from_purchase_cost = models.IntegerField(u"Процент от цена закупки на указаном складе")
    storage = models.ForeignKey(Storage) # для всех точек pickup в этом городе
    pickup_point = models.ForeignKey(PickupPoint) # для данной точки получения
    shop = models.ForeignKey(Shop)

    def is_allow_for_pickup_point(self, pickup_point):
        if pickup_point == self.pickup_point:
            return True
        return False

    def is_allow_for_pickup_city(self, pickup_city):
        if pickup_city == self.pickup_point.city:
            return True
        return False

    def is_allow_for_storage(self, storage):
        if storage == self.storage:
            return True
        return False

class RepositoryOfferProductsPrice(models.Model, Offer):
    """
    Берешь телефон вместе с чехол за 101000.
    При том что по одиночке телефон стоит 100000, а чехол 5000.
    """
    text = models.CharField(max_length=200)
    products = models.ManyToManyField(Product)
    price = models.IntegerField(u"Цена")
    currency = models.CharField(u"Валюта", max_length=5)
    shop = models.ForeignKey(Shop)

