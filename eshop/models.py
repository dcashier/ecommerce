#!-*-coding: utf-8 -*-
from django.db import models

# Create your models here.

class City(models.Model):
    title = models.CharField(max_length=200)

class Storage(models.Model):
    title = models.CharField(max_length=200)

class Pickup(models.Model):
    title = models.CharField(max_length=200)
    city = models.ForeignKey(City)

class ZoneCourier(models.Model):
    title = models.CharField(max_length=200)

class Building(models.Model):
    address = models.CharField(max_length=200)

class Product(models.Model):
    text = models.CharField(max_length=200)

class Order(models.Model):
    text = models.CharField(max_length=200)
    offers = []

    def add_offer(self, offer):
        self.offers.append(offer)

class Seller(models.Model):
    text = models.CharField(max_length=200)

class Shop(models.Model):
    title = models.CharField(max_length=200)
    pickup_points = models.ManyToManyField(Pickup)
    storages = models.ManyToManyField(Storage)
    sellers = models.ManyToManyField(Seller)
    #offers = models.ManyToManyField(Offer)

    #def add_offer_for_user_with_pickup_in_city(self, offer, pickup_in_city):
    #    self.offers.add(offer)

    def add_pickup(self, pickup_point):
        self.pickup_points.add(pickup_point)

    #def add_pickup_for_user_with_pickup_in_city(self, pickup_point, pickup_in_city):
    #    self.pickup_points.add(pickup_point)

    def add_storage(self, storage):
        self.storages.add(storage)

    def is_offer_pickup_in_city(self, offer, pickup_in_city):
        return True

    def is_order_issue_in_pickup_point(self, order, pickup_point):
        return True

    def is_order_pickup_in_city(self, order, pickup_in_city):
        return True

    def is_pickup_in_city(self, pickup_in_city):
        for pickup_point in self.pickup_points.all():
            if pickup_point.city == pickup_in_city:
                return True
        return False

    #def list_offer(self, session):
    def list_offer_for_user_with_pickup_in_city(self, user, pickup_in_city):
        #return sorted(list(self.offers.all()), key=lambda x : x.id)
        offers = []
        #for offer in self.offers.all():
        for offer in OfferProductPriceStoragePickuppoint.objects.all():
            #if self.is_offer_pickup_in_city(offer, pickup_in_city):
            #   offers.append(offer)
            #order = Order()
            #order.add_offer(offer)
            #if self.is_order_pickup_in_city(order, pickup_in_city):
            #    offers.append(offer)
            if offer.is_allow_for_pickup_city(pickup_in_city):
                offers.append(offer)
        return sorted(offers, key=lambda x : x.id)

    #def list_pickup(self, session, order):
    def list_pickup_for_user_with_pickup_in_city_with_order(self, user, pickup_in_city, order):
        #return sorted(list(self.pickup_points.all()), key=lambda x : x.id)
        pickup_points = []
        for pickup_point in self.pickup_points.all():
            if self.is_order_issue_in_pickup_point(order, pickup_point):
                pickup_points.append(pickup_point)
        return sorted(pickup_points, key=lambda x : x.id)

    #def list_storage(self, session, order):
    def __list_storage_for_user_with_pickup_in_city_with_order(self, user, pickup_in_city, order):
        return sorted(list(self.storages.all()), key=lambda x : x.id)

    def test_list_storage_for_user_with_pickup_in_city_with_order(self, user, pickup_in_city, order):
        return self.__list_storage_for_user_with_pickup_in_city_with_order(user, pickup_in_city, order)



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

class OfferProductPrice(models.Model, Offer):
    """
    самый простой цена и продукт
    """
    text = models.CharField(max_length=200)
    product = models.ForeignKey(Product)
    price = models.IntegerField(u"Цена")
    currency = models.CharField(u"Валюта", max_length=5)
    shop = models.ForeignKey(Shop)

class OfferProductPriceQuantity(models.Model, Offer):
    """
    для отовиков, за единоверменную покупку 10 штук суммарно заплатите на 5% меньше.
    """
    text = models.CharField(max_length=200)
    product = models.ForeignKey(Product)
    price = models.IntegerField(u"Цена")
    currency = models.CharField(u"Валюта", max_length=5)
    quantity = models.IntegerField(u"Штук")
    shop = models.ForeignKey(Shop)

class OfferProductPricePickupcity(models.Model, Offer):
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

class OfferProductPricePickuppoint(models.Model, Offer):
    """
    Хотим разрекламировать новый магазин и там слали специальные цены.
    """
    text = models.CharField(max_length=200)
    product = models.ForeignKey(Product)
    price = models.IntegerField(u"Цена")
    currency = models.CharField(u"Валюта", max_length=5)
    pickup_point = models.ForeignKey(Pickup) # для данной точки получения
    shop = models.ForeignKey(Shop)

    def is_allow_for_pickup_point(self, pickup_point):
        if pickup_point == self.pickup_point:
            return True
        return False

    def is_allow_for_pickup_city(self, pickup_city):
        if pickup_city == self.pickup_point.city:
            return True
        return False

class OfferProductPriceStorage(models.Model, Offer):
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

class OfferProductPriceStoragePickuppoint(models.Model, Offer):
    """
    Для точки получения в Москве если товар едет с московского склада цена одна, а если точка получения на Сахалинее и товар едет также с московского скалада то цена будет другой.
    """
    text = models.CharField(max_length=200)
    product = models.ForeignKey(Product)
    price = models.IntegerField(u"Цена")
    currency = models.CharField(u"Валюта", max_length=5)
    storage = models.ForeignKey(Storage) # для всех точек pickup в этом городе
    pickup_point = models.ForeignKey(Pickup) # для данной точки получения
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

class OfferProductPrecentfrompurchasecostStoragePickuppoint(models.Model, Offer):
    """
    Для точеки получения на Сахалинее, если товар едет с московского скалада то цена будет на 10% процентов выше по сравнению с ценой закупки(у товара на складе в этом случае должна быть цена закупки), а если точка получения в Москве то всего на 3%.
    """
    text = models.CharField(max_length=200)
    product = models.ForeignKey(Product)
    precent_from_purchase_cost = models.IntegerField(u"Процент от цена закупки на указаном складе")
    storage = models.ForeignKey(Storage) # для всех точек pickup в этом городе
    pickup_point = models.ForeignKey(Pickup) # для данной точки получения
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

class OfferProductsPrice(models.Model, Offer):
    """
    Берешь телефон вместе с чехол за 101000.
    При том что по одиночке телефон стоит 100000, а чехол 5000.
    """
    text = models.CharField(max_length=200)
    products = models.ManyToManyField(Product)
    price = models.IntegerField(u"Цена")
    currency = models.CharField(u"Валюта", max_length=5)
    shop = models.ForeignKey(Shop)


class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

class Session(models.Model):
    user = models.ForeignKey(User)
    city = models.ForeignKey(City)

class CatalogShops(models.Model):
    title = models.CharField(max_length=200)
    shops = models.ManyToManyField(Shop)

    #def allow_shops_for_session(self, session):
    def allow_shops_for_user_with_pickup_in_city(self, user, pickup_in_city):
        #return sorted(list(self.shops.all()), key=lambda x : x.id)
        shops = []
        for shop in self.shops.all():
            if shop.is_pickup_in_city(pickup_in_city):
                shops.append(shop)
        return sorted(shops, key=lambda x : x.id)

    def add_shop(self, shop):
        self.shops.add(shop)

    #def add_shop_for_user_with_pickup_in_city(self, shop, pickup_in_city):
    #    self.shops.add(shop)


#class Poll(models.Model):
#    question = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')
#
#class Choice(models.Model):
#    poll = models.ForeignKey(Poll)
#    choice = models.CharField(max_length=200)
#    votes = models.IntegerField()
