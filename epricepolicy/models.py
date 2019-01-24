#!-*-coding: utf-8 -*-
from django.db import models
from eproduct.models import *
from estorage.models import *

class PriceFactoryPartPurchaseCost(models.Model):
    precent = models.IntegerField(u"Процент")

    def generate(self, purchase_cost, product, storage):
        return purchase_cost * (100 + self.precent) / 100

class PriceFactoryPartPurchaseCostFromStock(models.Model):
    """
    Наценка на любой продукт : самый простой подход создаем наценку на в 10% от закупочной цены на все продукты.
    """
    precent = models.IntegerField(u"Процент, цена зависит от цены закупки которая указана в остатках склада, на которм лежит продукт")

    def generate(self, purchase_cost, product, storage):
        purchase_costs = set()
        #for stock in storage.stocks_by_product(product):
        #    purchase_costs.add(stock.purchase_cost)
        for purchase_cost in storage.list_purchase_cost_for_product(product):
            purchase_costs.add(purchase_cost)

        if not len(purchase_costs) == 1:
            raise ValidationError(u"Не допусимое количество цен закупки для одного склада")

        return list(purchase_costs)[0] * (100 + self.precent) / 100

class PriceFactoryFix(models.Model):
    price = models.IntegerField(u"Цена")
    currency = models.CharField(u"Валюта", max_length=5)

    def generate(self, purchase_cost, product, storage):
        return self.price

class PricePolicy(models.Model):
    filter_produce = models.ManyToManyField(FilterProductCrossIdCategoryBrand)
    filter_storage = models.ManyToManyField(FilterStorageId)
    filter_pickup_point = models.ManyToManyField(FilterPickupPointIdCity)

    price_factory_part_purchase_cost = models.ManyToManyField(PriceFactoryPartPurchaseCost)
    price_factory_part_purchase_cost_from_stock = models.ManyToManyField(PriceFactoryPartPurchaseCostFromStock)
    price_factory_fix = models.ManyToManyField(PriceFactoryFix)

    def is_allow_product_quantity_storage_pickup_point(self, product, quantity, storage, pickup_point):
        return True

    def allow_price_factory(self, product, quantity, storage, pickup_point):
        price_factories = []
        if self.is_allow_product_quantity_storage_pickup_point(product, quantity, storage, pickup_point):
            for price_factory in self.price_factory_part_purchase_cost.all():
                price_factories.append(price_factory)
            for price_factory in self.price_factory_part_purchase_cost_from_stock.all():
                price_factories.append(price_factory)
            for price_factory in self.price_factory_fix.all():
                price_factories.append(price_factory)
        return price_factories
