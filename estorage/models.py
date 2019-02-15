#!-*-coding: utf-8 -*-
from django.db import models
from eproduct.models import *
from epartnumber.models import *

#### Region

class Region(models.Model):
    title = models.CharField(max_length=200)

#### City

class City(models.Model):
    title = models.CharField(max_length=200)
    region = models.ForeignKey(Region)

class FilterCityIdRegion(models.Model):
    pickup_points = models.ManyToManyField(City)
    regions = models.ManyToManyField(Region)

#### Storage

class Storage(models.Model):
    title = models.CharField(max_length=200)
    size = models.IntegerField(u"Максимальное количество штук различных позиций, которое может принять склад.")

    def quantity(self, product):
        quantity = 0
        for stock in Stock.objects.filter(storage=self, product=product):
            #quantity += stock.quantity
            if stock.has:
                quantity += stock.quantity
            else:
                quantity -= stock.quantity
        return quantity

    def __has(self, product, quantity):
        if self.quantity(product) >= quantity:
            return True
        return False

    def __has_free_place(self, product, quantity):
        if self.quantity_all() + quantity < self.size:
            return True
        return False

    def __stocks(self, product):
        stocks = []
        for stock in Stock.objects.filter(storage=self, product=product, has=True):
            for stock_element in stocks:
                if stock.part_number == stock_element['part_number']:
                    stock_element['quantity'] += stock.quantity
                    break
            else:
                stocks.append({
                    'part_number': stock.part_number,
                    'quantity': stock.quantity,
                })

        for stock in Stock.objects.filter(storage=self, product=product, has=False):
            for stock_element in stocks:
                if stock.part_number == stock_element['part_number']:
                    stock_element['quantity'] -= stock.quantity
                    break
            else:
                # Списали того чего не было
                assert False

        stock_object = []
        for stock in stocks:
            if stock['quantity'] < 0:
                assert False
            elif stock['quantity'] > 0:
                stock_object.append(Stock(product=product, quantity=stock['quantity'], storage=self, part_number=stock['part_number'], has=True))
        return stock_object

    def list_product(self):
        products = set()
        for stock in Stock.objects.filter(storage=self):
            products.add(stock.product)
        return list(products)

    def list_part_number_for_product(self, product):
        part_numbers = set()
        for stock in Stock.objects.filter(storage=self, product=product):
            part_numbers.add(stock.part_number)
        return list(part_numbers)

    def __load(self, has, product, quantity, part_number):
        stock = Stock(product=product, quantity=quantity, storage=self, part_number=part_number, has=has)
        stock.save()

    def pull(self, product, quantity):
        if not self.__has(product, quantity):
            assert False
        #cargo = []

        # Сформировать обеспеченные остатки
        # Удалять уже из обеспеченных

        #stocks = []
        #for stock in Stock.objects.filter(storage=self, product=product, has=True):
        #    for stock_element in stocks:
        #        if stock.part_number == stock_element['part_number']:
        #            stock_element['quantity'] += stock.quantity
        #            break
        #    else:
        #        stocks.append({
        #            'part_number': stock.part_number,
        #            'quantity': stock.quantity,
        #        })

        #for stock in Stock.objects.filter(storage=self, product=product, has=False):
        #    for stock_element in stocks:
        #        if stock.part_number == stock_element['part_number']:
        #            stock_element['quantity'] -= stock.quantity
        #            break
        #    else:
        #        # Списали того чего не было
        #        assert False


        #for stock in stocks:
        #    if quantity >= stock.quantity:
        #        unload_quantity = stock.quantity
        #    else:
        #        unload_quantity = quantity
        #    #self.__unload(stock, unload_quantity)
        #    #XXX Тут ошибка и тесты должны ее выявить
        #    #self.__load(False, stock.product, quantity, stock.part_number)
        #    self.__load(False, stock.product, unload_quantity, stock.part_number)
        #    quantity -= unload_quantity
        #    #cargo.append({
        #    #    'product': product,
        #    #    'quantity': quantity,
        #    #})
        #    if quantity == 0:
        #        break
        #    elif quantity < 0:
        #        assert False
        #for stock in stocks:
        #    if quantity >= stock['quantity']:
        #        unload_quantity = stock['quantity']
        #    else:
        #        unload_quantity = quantity
        #    self.__load(False, product, unload_quantity, stock['part_number'])
        #    quantity -= unload_quantity
        #    if quantity == 0:
        #        break
        #    elif quantity < 0:
        #        assert False
        stocks = self.__stocks(product)
        for stock in stocks:
            if quantity >= stock.quantity:
                unload_quantity = stock.quantity
            else:
                unload_quantity = quantity
            self.__load(False, product, unload_quantity, stock.part_number)
            quantity -= unload_quantity
            if quantity == 0:
                break
            elif quantity < 0:
                assert False

        if quantity > 0:
            assert False

    def push(self, product, quantity, part_number):
        #TODO проверить есть ли свободное место на складе чтобы принять такой обем груза
        if not self.__has_free_place(product, quantity):
            assert False
        self.__load(True, product, quantity, part_number)

    def quantity_all(self):
        quantity = 0
        for stock in Stock.objects.filter(storage=self):
            #quantity += stock.quantity
            if stock.has:
                #print quantity, '+=', stock.quantity
                quantity += stock.quantity
                #print quantity
            else:
                #print quantity, '-=', stock.quantity
                quantity -= stock.quantity
                #print quantity
        return quantity

    #def __unload(self, stock, quantity):
    #    self.__load(False, stock.product, quantity, stock.part_number)


class Stock(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(u"Количество")
    storage = models.ForeignKey(Storage)
    part_number = models.ForeignKey(PartNumber)
    has = models.BooleanField(verbose_name=u'Пришоло на склад', default=True)

class FilterStorageId(models.Model):
    storages = models.ManyToManyField(Storage)

#### PickupPoint

class PickupPoint(models.Model):
    title = models.CharField(max_length=200)
    city = models.ForeignKey(City)

    def get_city(self):
        return self.city

    def is_null(self):
        return False

class FilterPickupPointIdCity(models.Model):
    pickup_points = models.ManyToManyField(PickupPoint)
    cities = models.ManyToManyField(City)
