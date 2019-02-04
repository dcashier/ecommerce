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

    def calculate_revards_balls_for_last_order(self):
        print 'Alert : Not work calculate_revards_balls_for_last_order'
        return 3000

    def change_status_for_last_order(self, status):
        print 'Alert : Not work change_status_for_last_order'

    def check_payment_for_last_order(self):
        print 'Alert : Not work check_payment_for_last_order'
        return True

    def create_client_shop_with_phone_number(self, shop, phone_number):
        client = Shop(phone_number=phone_number)
        client.save()
        self.shop.clients.add(client)

    def create_order(self, parmas):
        """
        Следует указать:
            что
            из какой партии
            в каком количекстве
            с каких складов
            на кокие наточки выдачи
            за какую сумму реализуются позиции
            на основе каких ценовых политик была сформирована цена реализации
            в какой срок будет доставлен весь товар на указанные точки выдачи
            для какого контрагента

        Т.е. заказ это некий набор обьедиенных действий!
        """
        pass

    def create_payemnt_link_for_last_order(self):
        print 'Alert : Not work create_payemnt_link_for_last_order'

    def create_price_last_order(self):
        print 'Alert : Not work create_price_last_order'


    def __error_by_order(self, order_params):
        """
        Проверить наличие доступных остатков во всей сети.
        Проверить наличие доступных остатков для данных параметров заказа.
            А при создании заказа надо еще и зараезрвировать их чтобы они не ушли под другой заказ.
        Проверить что цены на позиции в заказе установлены верно(не продаем товары за рубль хотя его реальная стомость миллион).
        Проверить возможность продажи всех товаров из заказа в данном регионе, в городе, на точке самовывоза.
        Проверить что все позиции по данному заказу каким либо образом можно доставить на точку самовывоза.
        Проверить что весь заказ будет точке самовывоза в установелнный срок.
        Проверить что лимит на такие заказы не привышен.

        order_params = {
            'version': 'v1',
            'basket': [
                {
                    'product'
                    'quantity'
                    'price'
                    'currency'
                },
                {},
            ],
            'pickup': {
                'point'
                'interval'
            },
            'seller'
            'client'
        }

        Провести тест когда в корзине один и тотже товар присутствует несколько раз но с разным колличеством.
            Проверить что не только колличество разное но и цена.
        """
        #order_params - переписать на объект который используется для проверики и создания заказов разных версий.
        products = [element['product'] for element in order_params['basket']]
        prices_products = [[element['price'], element['product']] for element in order_params['basket']]
        quantity_products = [[element['quantity'], element['product']] for element in order_params['basket']]
        #client = order_params['client']
        client_city = order_params['pickup']['point'].get_city()
        client_type = None

        for quantity_product in quantity_products:
            if quantity_product[0] > self.quantity_for_sale(quantity_product[1]):
                return 'Error : Not find allow quantity %s for sale product %s' % (quantity_product[0], quantity_product[1])
        for price_product in prices_products:
            if not price_product[0] in self.prices(price_product[1], client_city, client_type):
                return 'Error : Price %s not allow for product %s.' % (price_product[0], price_product[1])
        if not len(products) == len(self.list_allow_product_for_client(products, client_city, client_type)):
            return 'Error : Same product not allow for sale'
        return None

    def get_client_shop_with_phone_number(self, shop, phone_number):
        if not self.__is_seller_work_in_shop(shop):
            raise ValidationError(u"Выбранынй прожавец не работает в указханном магазине.")
        for client in Shop.objects.filter(phone_number=phone_number): # не безопасно
            return client
        raise ValidationError(u"У магазина ент клиента с таким телефоном.")

    def has_shop_client_with_phone_number(self, shop, phone_number):
        if not self.__is_seller_work_in_shop(shop):
            raise ValidationError(u"Выбранынй прожавец не работает в указханном магазине.")
        for client in Shop.objects.filter(phone_number=phone_number): # не безопасно
            if self.has_shop_client(shop, client):
                return True
        return False

    def has_shop_client(self, shop, client):
        print self.shop.clients.all()
        print shop
        print self.__is_seller_work_in_shop(shop)
        print client
        print '---'
        if self.__is_seller_work_in_shop(shop) and client in self.shop.clients.all():
            return True
        print 'FFF'
        return False

    def is_allow_order(self, order_params):
        error = self.__error_by_order(order_params)
        if error:
            #print error
            return False
        return True

    def __is_allow_product_for_client(self, product, client_city, client_type):
        print 'check Rule'
        print 'check Delivery'
        print 'check Quantity for Sale'
        return True

    def is_delivery(self, product, storage, point_pickup):
        #if point_pickup.id == 2:
        #    return False
        return True

    def __is_seller_work_in_shop(self, shop):
        if self.shop and self.shop == shop:
            return True
        return False

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

    def list_allow_product_for_client(self, products, client_city, client_type):
        allow_products = []
        for product in products:
            if self.__is_allow_product_for_client(product, client_city, client_type):
                allow_products.append(product)
        return allow_products

    def list_product_in_stock(self, category):
        storages = self.shop.storages.all()
        products = set()
        for storage in storages:
            for product in storage.list_product():
                products.add(product)
        return list(products)

    def pickup_points(self, params_basket, client_city, client_type):
        """
        Попробуем доставить с каждого возможного склада на каждую возможную точку выдачи,
            столько сколько есть в наличии на складе.
        И посчитаем сколько товаров из корзины смогли доставить на каждую точку.
        Если количество доставленных совпадает с количеством в корзине то данная точка подходит.
        """
        pickup_points_and_count_product_was_delivery = {}
        for element in params_basket:
            product = element['product']
            quantity = element['quantity']
            for point_pickup in filter(lambda pp : pp.city == client_city, self.shop.pickup_points.all()):
                quantity_was_delivery = 0
                for storage in self.shop.storages.all():
                    if quantity <= quantity_was_delivery:
                        break
                    if self.is_delivery(product, storage, point_pickup):
                        quantity_was_delivery += self.__quantity_for_sale_on_storage(product, storage)

                if quantity <= quantity_was_delivery:
                    pickup_points_and_count_product_was_delivery.setdefault(point_pickup, 0)
                    pickup_points_and_count_product_was_delivery[point_pickup] += 1

        pickup_points_allow_for_basket = []
        for pickup_point, count in pickup_points_and_count_product_was_delivery.items():
            if len(params_basket) == count:
                pickup_points_allow_for_basket.append(pickup_point)

        return pickup_points_allow_for_basket

    def __price_factories_allow_for_situation_one_product(self, product, storage, pickup_point):
        quantity = 1
        price_factories = []
        for price_policy in self.price_policies.all():
            for price_factory in price_policy.allow_price_factory(product, quantity, storage, pickup_point):
                price_factories.append(price_factory)
        return price_factories

    def prices(self, product, client_city, client_type):
        pickup_points = self.shop.pickup_points.all()
        storages = self.shop.storages.all()
        quantity = 1
        link_price_product_storage_pickup_point = self.__link_price_product_storage_pickup_point(product, storages, pickup_points)
        prices = set()
        for link in link_price_product_storage_pickup_point:
            price = link['price']
            prices.add(price)
        return sorted(list(prices))

    def quantity_for_sale(self, product):
        storages = self.shop.storages.all()
        quantity = 0
        for storage in storages:
            quantity += self.__quantity_for_sale_on_storage(product, storage)
        return quantity

    def __quantity_for_sale_on_storage(self, product, storage):
        quantity = storage.quantity(product)
        for reserve in Reserve.objects.filter(storage=storage, product=product):
            quantity -= reserve.quantity
            if quantity < 0:
                raise ValidationError(u"Не коректное количество остатоков. Хотя приконкурентном взаимодействии могут продать больше чем есть в наличии, и тогда такая ситуация возможна")
        return quantity

    def reserve_product_on_storage(self, product, quantity, storage, info_text, part_number):
        reserve = Reserve(product=product, quantity=quantity, storage=storage, part_number=part_number)
        reserve.save()

    def shops(self):
        return [self.shop]


class Customer(object):
    def set_payment_balls_for_last_order(self, balls):
        pass

    def pay_by(self, link_for_payment):
        pass

