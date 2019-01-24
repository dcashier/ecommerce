#!-*-coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from eproduct.models import *
from estorage.models import *
from epartnumber.models import *
from ereserve.models import *
from epricepolicy.models import *
#from eoffer.models import *
from epurchase.models import *
from esale.models import *
from eshop.models import *

class Seller(models.Model):
    """
    Продавец решает какую политику формирования цены применить в данном случае
    product, purchase cost, client(type), shop, storage, pickup point, seller
    Продавец это может быть и человек в магазине на улице, и сайт, и телеграм бот, и человек в кол центре
    """
    title = models.CharField(max_length=100)
    shop = models.ForeignKey(Shop)
    price_policies = models.ManyToManyField(PricePolicy) # политики которые может использовать данный продавец ему назанчаются свыше

    def quantity_for_sale(self, product):
        storages = self.shop.storages.all()
        quantity = 0
        for storage in storages:
            quantity += storage.quantity(product)
            for reserve in Reserve.objects.filter(storage=storage, product=product):
                quantity -= reserve.quantity
                if quantity < 0:
                    raise ValidationError(u"Не коректное количество остатоков. Хотя приконкурентном взаимодействии могут продать больше чем есть в наличии, и тогда такая ситуация возможна")
        return quantity

    def __is_allow_product_for_client(self, product, client_city, client_type):
        print 'check Rule'
        print 'check Delivery'
        print 'check Quantity for Sale'
        return True

    def __price_factories_allow_for_situation_one_product(self, product, storage, pickup_point):
        quantity = 1
        price_factories = []
        for price_policy in self.price_policies.all():
            for price_factory in price_policy.allow_price_factory(product, quantity, storage, pickup_point):
                price_factories.append(price_factory)
        return price_factories

    def __link_price_factory_product_storage_pickup_point(self, product, storages, pickup_points):
        link_price_factory_product_storage_pickup_point = []
        for storage in storages:
            for pickup_point in pickup_points:
                for price_factory in self.__price_factories_allow_for_situation_one_product(product, storages, pickup_points):
                    link_price_factory_product_storage_pickup_point.append({
                        'product': product,
                        'storage': storage,
                        'pickup_point': pickup_point,
                        'price_factory': price_factory,
                    })
        return link_price_factory_product_storage_pickup_point

    def __link_price_product_storage_pickup_point(self, product, storages, pickup_points):
        link_price_product_storage_pickup_point = []
        for storage in storages:
            for pickup_point in pickup_points:
                for price_factory in self.__price_factories_allow_for_situation_one_product(product, storages, pickup_points):
                    for part_number in storage.list_part_number_for_product(product):
                        purchase_costs = set()
                        for element_purchase in ElemetPurchase.objects.filter(product=product, part_number=part_number):
                            link_price_product_storage_pickup_point.append({
                                'product': product,
                                'storage': storage,
                                'pickup_point': pickup_point,
                                'part_number': part_number,
                                'price': price_factory.generate(element_purchase.purchase_cost, product, storage),
                            })
        return link_price_product_storage_pickup_point

    def generate_prices(self, product, client_city, client_type):
        pickup_points = self.shop.pickup_points.all()
        storages = self.shop.storages.all()
        quantity = 1
        link_price_product_storage_pickup_point = self.__link_price_product_storage_pickup_point(product, storages, pickup_points)
        prices = set()
        for link in link_price_product_storage_pickup_point:
            price = link['price']
            prices.add(price)
        return sorted(list(prices))

    def list_allow_product_for_client(self, products, client_city, client_type):
        allow_products = []
        for product in products:
            if self.__is_allow_product_for_client(product, client_city, client_type):
                allow_products.append(product)
        return allow_products

    def list_product(self, category):
        storages = self.shop.storages.all()
        products = set()
        for storage in storages:
            for product in storage.list_product():
                products.add(product)
        return list(products)

    def reserve_product_on_storage(self, product, quantity, storage, info_text, part_number):
        reserve = Reserve(product=product, quantity=quantity, storage=storage, part_number=part_number)
        reserve.save()
