#!-*-coding: utf-8 -*-
from django.db import models

# Create your models here.

class City(models.Model):
    title = models.CharField(max_length=200)

class PickupPoint(models.Model):
    title = models.CharField(max_length=200)
    city = models.ForeignKey(City)

class ZoneCourier(models.Model):
    title = models.CharField(max_length=200)

class Building(models.Model):
    address = models.CharField(max_length=200)

class Brand(models.Model):
    text = models.CharField(max_length=200)

class Category(models.Model):
    text = models.CharField(max_length=200)

class Product(models.Model):
    text = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
    brand = models.ForeignKey(Brand)

class Storage(models.Model):
    title = models.CharField(max_length=200)

class Stock(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(u"Количество")
    storage = models.ForeignKey(Storage)
    purchase_cost = models.DecimalField(u"стоимость закупки одной штуки", decimal_places=2, max_digits=7)
    currency = models.CharField(u"Валюта", max_length=5)

class Order(models.Model):
    text = models.CharField(max_length=200)
    offers = []

    def add_offer(self, offer):
        self.offers.append(offer)

#class Seller(models.Model):
#    text = models.CharField(max_length=200)

class Shop(models.Model):
    title = models.CharField(max_length=200)
    pickup_points = models.ManyToManyField(PickupPoint)
    storages = models.ManyToManyField(Storage)
    #sellers = models.ManyToManyField(Seller)
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

    def is_allow_storage(self, storage):
        if storage in self.storages.all():
            return True
        return False

    #def list_offer(self, session):
    def list_offer_for_user_with_pickup_in_city(self, user, pickup_in_city):
        #return sorted(list(self.offers.all()), key=lambda x : x.id)
        offers = []
        #for offer in self.offers.all():
        for offer in RepositoryOfferProductPriceStoragePickuppoint.objects.all():
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


class PriceFactoryPartPurchaseCostFromStock(models.Model):
    """
    Наценка на любой продукт : самый простой подход создаем наценку на в 10% от закупочной цены на все продукты.
    """
    precent = models.IntegerField(u"Процент, цена зависит от цены закупки которая указана в остатках склада, на которм лежит продукт")

    def generate_from_purchase_cost(self, purchase_cost):
        return purchase_cost * self.precent

    def generate_for_product_on_storage(self, product, storage):
        purchase_costs = set()
        for stock in storage.stocks_by_product():
            purchase_costs.add(stock.purchase_cost)

        if not len(purchase_costs) == 1:
            raise ValidationError(u"Не допусимое количество цен закупки для одного склада")

        return purchase_costs[0] * self.precent

class PriceFactoryFix(models.Model):
    price = models.IntegerField(u"Цена")
    currency = models.CharField(u"Валюта", max_length=5)

class FilterProduct(object):
    pass

class FilterProductCrossIdCategoryBrand(models.Model, FilterProduct):
    products = models.ManyToManyField(Product)
    categories = models.ManyToManyField(Category)
    brands = models.ManyToManyField(Brand)

class FilterPickupPoint(object):
    pass

class FilterPickupPointIdCity(models.Model, FilterPickupPoint):
    pickup_points = models.ManyToManyField(PickupPoint)
    cities = models.ManyToManyField(City)

class FilterStorage(object):
    pass

class FilterStorageId(models.Model, FilterStorage):
    storages = models.ManyToManyField(Storage)

class PricePolicy(models.Model):
    filter_produce = models.ManyToManyField(FilterProductCrossIdCategoryBrand)
    filter_storage = models.ManyToManyField(FilterStorageId)
    filter_pickup_point = models.ManyToManyField(FilterPickupPointIdCity)

    price_factory_part_purchase_cost_from_stock = models.ManyToManyField(PriceFactoryPartPurchaseCostFromStock)
    price_factory_fix = models.ManyToManyField(PriceFactoryFix)

    def allow_price_factory(product, quantity, storage, pickup_point):
        price_factories = []
        if price_policy.is_allow_product_quantity_storage_pickup_point(product, quantity, storage, pickup_point):
            for price_factory in self.factory_price_part_purchase_cost_from_stock.all():
                price_factories.append(factory)
            for price_factory in self.factory_price_fix.all():
                price_factories.append(factory)
        return price_factories


class Seller(models.Model):
    """
    Продавец решает какую политику формирования цены применить в данном случае
    product, purchase cost, client(type), shop, storage, pickup point, seller
    """
    title = models.CharField(max_length=100)
    shop = models.ForeignKey(Shop)

    price_policies = models.ManyToManyField(PricePolicy)

    def __get_price_factories_allow_for_situation_one_product(self, product, storage, pickup_point):
        quantity = 1
        price_factories = []
        for price_policy in self.price_policies.all():
            for price_factory in price_policy.allow_price_factory(product, quantity, storage, pickup_point):
                price_factories.append(price_factory)
        return price_factories

    def generate_prices(self, product, client_city, client_type):
        pickup_points = self.shop.pickup_points_in_city(client_city)
        storages = self.shop.allow_storages()
        quantity = 1

        price_factories = set()
        for storage in storages:
            for pickup_point in pickup_points:
                for price_factory in self.__get_price_factories_allow_for_situation_one_product(product, storage, pickup_point):
                    price_factories.add(price_factory)

        prices = set()
        for price_factory in price_factories:
            price = price_factory.generate_for_product_on_storage(product, storage)
            prices.add(price)

        return prices

    #def get_factory_allow_for_situation_many_diffirent_stocks(self, [{product, quantity, storage], {}], pickup_point):
    #    pass


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
