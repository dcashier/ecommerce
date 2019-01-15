from django.db import models

# Create your models here.

class Storage(models.Model):
    title = models.CharField(max_length=200)

class Pickup(models.Model):
    title = models.CharField(max_length=200)

class ZoneCourier(models.Model):
    title = models.CharField(max_length=200)

class Building(models.Model):
    address = models.CharField(max_length=200)

class Producr(models.Model):
    text = models.CharField(max_length=200)

class Offer(models.Model):
    text = models.CharField(max_length=200)

class Order(models.Model):
    text = models.CharField(max_length=200)
    offers = []

    def add_offer(self, offer):
        self.offers.append(offer)

class Shop(models.Model):
    title = models.CharField(max_length=200)
    offers = models.ManyToManyField(Offer)
    pickup_points = models.ManyToManyField(Pickup)
    storages = models.ManyToManyField(Storage)

    def add_offer_for_user_with_pickup_in_city(self, offer, pickup_in_city):
        self.offers.add(offer)

    def add_pickup_for_user_with_pickup_in_city(self, pickup_point, pickup_in_city):
        self.pickup_points.add(pickup_point)

    def add_storage(self, storage):
        self.storages.add(storage)

    def is_pickup_in_city(self, pickup_in_city):
        return True

    #def list_offer(self, session):
    def list_offer_for_user_with_pickup_in_city(self, user, pickup_in_city):
        return sorted(list(self.offers.all()), key=lambda x : x.id)

    #def list_pickup(self, session, order):
    def list_pickup_for_user_with_pickup_in_city_with_order(self, user, pickup_in_city, order):
        return sorted(list(self.pickup_points.all()), key=lambda x : x.id)

    #def list_storage(self, session, order):
    def list_storage_for_user_with_pickup_in_city_with_order(self, user, pickup_in_city, order):
        return sorted(list(self.storages.all()), key=lambda x : x.id)


class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

class City(models.Model):
    title = models.CharField(max_length=200)

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

    def add_shop_for_user_with_pickup_in_city(self, shop, pickup_in_city):
        self.shops.add(shop)


#class Poll(models.Model):
#    question = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')
#
#class Choice(models.Model):
#    poll = models.ForeignKey(Poll)
#    choice = models.CharField(max_length=200)
#    votes = models.IntegerField()
