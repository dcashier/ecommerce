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
#from esale.models import *
from eshop.models import *

class SessionClientComeToShop(object):
    """
    Взаимодействие с клиентом, в рамках этого взаимодействия определяется постепенно
    набор всех желаемых позиций заказа, сроки и место доствки, ...
    но срок жизни ограничен.
    Анализировать все обращения к ресурсу?
    """
    pass

class Owner(object):
    def add_seller_for_shop():
        pass

class SellerXS(object):
    def calculate_rewards_balls_for_order(self, order):
        loyalty = self.get_loyalty()
        return self.seller.calculate_rewards_balls_for_order(order, loyalty)

    def _create_customer(self, phone_number, title, sex, birthday, phone_number_referee, entrance_ball):
        executor = self.get_executor()
        if self.seller.has_shop_client_with_phone_number(executor, phone_number):
            raise ValidationError(u"Error : Сustomer already exists.")
        self.seller.create_customer(executor, phone_number, title, sex, birthday)

        if phone_number_referee:
            customer = self.seller.get_client_shop_with_phone_number(executor, phone_number)
            if self.seller.has_shop_client_with_phone_number(executor, phone_number_referee):
                referee = self.seller.get_client_shop_with_phone_number(executor, phone_number_referee)
                self.seller.add_referee(customer, referee)
            else:
                print 'Error : Not Find referee with phone_number_referee'

        if entrance_ball:
            customer = self.seller.get_client_shop_with_phone_number(executor, phone_number)
            self.seller.add_entrance_ball(customer, entrance_ball)

    def create_customer(self, phone_number, title, sex, birthday, phone_number_referee):
        entrance_ball = 0
        self._create_customer(phone_number, title, sex, birthday, phone_number_referee, entrance_ball)

    def create_customer_100(self, phone_number, title, sex, birthday, phone_number_referee):
        entrance_ball = 100
        self._create_customer(phone_number, title, sex, birthday, phone_number_referee, entrance_ball)

    def create_order(self, phone_number, price):
        pickup_point = self.get_pickup_point()
        self._create_order_pickup_point(phone_number, price, pickup_point)

    def _create_order_pickup_point(self, phone_number, price, pickup_point):
        """
        close
        """
        executor = self.get_executor()
        if not self.seller.has_shop_client_with_phone_number(executor, phone_number):
            self.seller.create_client_shop_with_phone_number(executor, phone_number)
        customer = self.seller.get_client_shop_with_phone_number(executor, phone_number)
        default_product = Product.objects.get(id=1)
        quantity = 1
        currency = "RUS"
        purchaser = Purchaser.get_purchaser_with_phone_number_for_client(phone_number, customer)
        if not self.seller.has_basket_for_client_in_shop(customer, executor):
            self.seller.create_basket_for_client_in_shop(customer, executor, purchaser)
        basket = self.seller.get_basket_for_client_in_shop(customer, executor)
        self.seller.add_product_in_basket(basket, default_product, quantity, price, currency)
        #pickup_point = PickupPoint.objects.get(id=1)
        self.seller.create_order_from_busket_and_pickup_point(customer, executor, purchaser, basket, pickup_point)
        basket.delete()

    def create_max_ball_in_loyalty(self, actor, price):
        loyalty = self.get_loyalty()
        return loyalty.create_range_ball(actor, price)[1]

    def get_balance_in_loyalty(self, actor, client):
        loyalty = self.get_loyalty()
        datetime_for_check = None
        return loyalty.get_balance(actor, client, datetime_for_check)

    def get_customer_order(self, order):
        return order.customer

    def get_client_with_phone_number(self, phone_number):
        return self.seller.get_client_shop_with_phone_number(self.get_executor(), phone_number)

    def get_customer(self, customer_id):
        return self.seller.get_customer(customer_id)

    def get_executor(self):
        if len(self.seller.list_executor()) > 1:
            raise ValidationError(u"Error : Do not use size XS.")
        return self.seller.list_executor()[0]

    def get_last_order_for_client_with_phone_number(self, phone_number):
        client = self.get_client_with_phone_number(phone_number)
        return self.get_last_order_for_client(client)

    def get_last_order_for_client(self, client):
        return self.seller.get_last_order_client(client)

    def get_loyalty(self):
        loyalties = self.seller.list_loyalty(self.get_executor())
        if len(loyalties) > 1:
            raise ValidationError(u"Error : Do not use size XS.")
        return loyalties[0]

    def get_object(self):
        return self.seller

    def get_max_percent_in_loyalty(self):
        loyalty = self.get_loyalty()
        return loyalty.get_max_percent()

    def get_order(self, order_id):
        return self.seller.get_order(order_id)

    def get_pickup_point(self):
        if self.seller.pickup_points.all().count() > 1:
            raise ValidationError(u"Error : Do not use size XS.")
        return self.seller.pickup_points.all()[0]

    def get_product(self, product_id):
        #TODO Нужна проверка прав доступа к заказу.
        return Product.objects.get(id=product_id)

    def has_customer_with_phone_number(self, phone_number):
        executor = self.get_executor()
        return self.seller.has_shop_client_with_phone_number(executor, phone_number)

    def has_order(self, order_id):
        return self.seller.has_order(order_id)

    def is_registration_in_loyalty(self, client):
        loyalty = self.get_loyalty()
        return True if loyalty.is_registration(self, client) else False

    def __init__(self, seller):
        self.seller = seller

    def list_order(self):
        executor = self.get_executor()
        pickup_point = self.get_pickup_point()
        return Order.objects.filter(executor=executor, pickup_point=pickup_point, seller=self.seller)

    def list_order_for_customer(self, customer):
        executor = self.get_executor()
        pickup_point = self.get_pickup_point()
        return Order.objects.filter(executor=executor, pickup_point=pickup_point, seller=self.seller, customer=customer).order_by('-id')

    def list_product(self):
        #TODO У каждого магазина должен быть свой набор продуктов или можно испоьзовать общий.
        # но не давать возможноть изменять никакой инфы по продуктам в базе, только создавать.
        # тогда будет общая база продуктов и в дальнейшем мапить не надо будет.
        products = []
        for product in Product.objects.all():
            if product.id != 1:
                products.append(product)
        return products
        #return self.seller.list_product()

    def list_shop(self):
        if len(self.seller.list_shop()) > 1:
            raise ValidationError(u"Error : Do not use size XS.")
        return self.seller.list_shop()

    def process_order_with_ball_type(self, order, ball_type):
        pickup_point = self.get_pickup_point()
        self._process_order_with_ball_type_pickup_point(order, ball_type, pickup_point)

    def _process_order_with_ball_type_pickup_point(self, order, ball_type, pickup_point):
        customer = self.get_customer_order(order)
        purchaser = Purchaser.objects.get(shop=customer)
        executor = self.get_executor()
        loyalty = self.get_loyalty()
        if ball_type == 'MAX':
            ball_for_spend = self.seller.max_allow_ball_for_spend_for_order(order, purchaser, customer, executor, loyalty)
        elif ball_type == 'ZERO':
            ball_for_spend = 0
        self.seller.process_order_without_customer_security(order, purchaser, customer, executor, loyalty, ball_for_spend, pickup_point)

    def registration_in_loyalty(self, client):
        loyalty = self.get_loyalty()
        executor = self.get_executor()
        loyalty.register_in_loyalty_hello_0(self, client, executor)


class SellerS(SellerXS):
    def create_order(self, phone_number, price, pickup_point):
        self._create_order_pickup_point(phone_number, price, pickup_point)

    def get_pickup_point_by_id(self, pickup_point_id):
        """
        Если права позволют работать сданной точкой
        """
        for pickup_point in self.seller.pickup_points.all():
            #print pickup_point.id, '==', pickup_point_id, pickup_point.id == pickup_point_id
            if pickup_point.id == pickup_point_id:
                return pickup_point
        assert False

    def __init__(self, seller):
        self.seller = seller
        self.order_repositiry = Order

    #def list_order(self, order_specification):
    def list_order(self):
        executor = self.get_executor()
        #pickup_point = self.get_pickup_point()

        order_specification = OrderSpecification()
        order_specification.pickup_points = list(self.seller.list_pickup_point())
        order_specification.executor = executor
        order_specification.seller = self.seller
        #return self.order_repositiry.list_order(order_specification)
        return Order.list_order(order_specification)
        #return Order.objects.filter(executor=executor, pickup_point=pickup_point, seller=self.seller)

    def list_shop(self):
        return self.seller.list_shop()

    def process_order_with_ball_type(self, order, ball_type, pickup_point):
        self._process_order_with_ball_type_pickup_point(order, ball_type, pickup_point)


class Purchaser(models.Model):
    title = models.CharField(max_length=100)
    shop = models.ForeignKey(Shop)
    phone_number = models.CharField(verbose_name=u'Телефонный номер', max_length=128, null=True, blank=True)

    @classmethod
    def get_purchaser_with_phone_number_for_client(cls, phone_number, client):
        return Purchaser.objects.get(phone_number=phone_number, shop=client)

    def __unicode__(self):
        return u"Purchaser (%s) : %s [customer : %s]" % (self.id, self.title, self.shop)


class Seller(models.Model):
    """
    Продавец решает какую политику формирования цены применить в данном случае
    product, purchase cost, client(type), shop, storage, pickup point, seller
    Продавец это может быть и человек в магазине на улице, и сайт, и телеграм бот, и человек в кол центре
    """
    title = models.CharField(max_length=100)
    shop = models.ForeignKey(Shop)
    pickup_points = models.ManyToManyField(PickupPoint, blank=True)
    #shop = models.ManyToManyField(Shop, blank=True)
    price_policies = models.ManyToManyField(PricePolicy, blank=True) # политики которые может использовать данный продавец ему назанчаются свыше

    def __accumulate_customer_ball_for_order(self, order, purchaser, customer, executor, loyalty):
        reward_ball = self.calculate_rewards_balls_for_order(order, loyalty)
        available_day = 90
        loyalty.transfer_ball(self, executor, customer, reward_ball, available_day)
        self.__change_status_for_order(order, u'Начислии балы клиенту по заказа')
        order.rewards_ball = reward_ball
        order.save()

    def add_product_in_basket(self, basket, product, quantity, price, currency):
        basket.add(product, quantity, price, currency)

    def calculate_rewards_balls_for_order(self, order, loyalty):
        return loyalty.calculate_reward(None, order.calculate_price())['ball']

    #def calculate_rewards_balls_for_order_xs(self, order):
    #    loyalty = self.get_loyalty_xs()
    #    return loyalty.calculate_reward(None, order.calculate_price())['ball']

    def __change_status_for_order(self, order, status):
        pass

    def check_payment_for_last_order(self):
        print 'Alert : Not work check_payment_for_last_order'
        return True

    def count_order_customer(self, customer):
        return Order.objects.filter(customer=customer).count()

    def create_basket_for_client_in_shop(self, client, shop, purchaser):
        basket = Basket(seller=self, customer=client, executor=shop, purchaser=purchaser)
        basket.save()

    def create_client_shop_with_phone_number(self, shop, phone_number):
        if not self.is_work_in_shop(shop):
            raise ValidationError(u"Выбранный прожавец не работает в указханном магазине.")
        client = Shop(phone_number=phone_number)
        client.save()
        self.shop.clients.add(client)
        purchaser = Purchaser(title=u"Default purchaser when Seller create Client.", shop=client, phone_number=phone_number)
        purchaser.save()

    def create_customer(self, executor, phone_number, title, sex, birthday):
        if not self.is_work_in_shop(executor):
            raise ValidationError(u"Выбранный прожавец не работает в указханном магазине.")
        client = Shop(phone_number=phone_number, title=title, sex=sex, birthday=birthday)
        client.save()
        self.shop.clients.add(client)
        purchaser = Purchaser(title=u"Default purchaser when Seller create Client.", shop=client, phone_number=phone_number)
        purchaser.save()


    #def create_easy_order_xs(self, phone_number, price):
    #    pickup_point = self.get_pickup_point_xs()
    #    self.create_easy_order_by_phone_number_of_customer(phone_number, price, pickup_point)

    #def create_easy_order_by_phone_number_of_customer(self, phone_number, price, pickup_point):
    #    executor = self.get_executor()
    #    if not self.has_shop_client_with_phone_number(executor, phone_number):
    #        self.create_client_shop_with_phone_number(executor, phone_number)
    #    customer = self.get_client_shop_with_phone_number(executor, phone_number)
    #    default_product = Product.objects.get(id=1)
    #    quantity = 1
    #    currency = "RUS"
    #    purchaser = Purchaser.get_purchaser_with_phone_number_for_client(phone_number, customer)
    #    if not self.has_basket_for_client_in_shop(customer, executor):
    #        self.create_basket_for_client_in_shop(customer, executor, purchaser)
    #    self.create_basket_for_client_in_shop(customer, executor, purchaser)
    #    basket = self.get_basket_for_client_in_shop(customer, executor)
    #    self.add_product_in_basket(basket, default_product, quantity, price, currency)
    #    #pickup_point = PickupPoint.objects.get(id=1)
    #    self.create_order_from_busket_and_pickup_point(customer, executor, purchaser, basket, pickup_point)
    #    basket.delete()

    def create_order_from_busket_and_pickup_point(self, client, shop, purchaser, basket, pickup_point):
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
        #print 'Alert : Not work create_order_from_busket_and_pickup_point'
        order = Order(
            customer=client,
            executor=shop,
            purchaser=purchaser,
            seller=self,
            pickup_point=pickup_point,
        )
        order.save()
        for basket_element in basket.elements():
            order.add(basket_element.product, basket_element.quantity, basket_element.price, basket_element.currency)

        #create_datetime = models.DateTimeField(u'дата и время создание заказа')
        #pickup_dateteme = models.DateTimeField(u'дата и время вручения всего заказа(т.е. последней партии)')

        #loyalty_ball = models.IntegerField(u"Оплаено балами.")

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

    def get_basket_for_client_in_shop(self, client, shop):
        for basket in Basket.objects.filter(customer=client, executor=shop):
            return basket
        raise ValidationError(u"Не нашли корзину клиента в укаханоом магазине.")

    def get_client_shop_with_phone_number(self, shop, phone_number):
        if not self.is_work_in_shop(shop):
            raise ValidationError(u"Выбранный прожавец не работает в указханном магазине.")
        for client in Shop.objects.filter(phone_number=phone_number): # не безопасно
            return client
        raise ValidationError(u"У магазина ент клиента с таким телефоном.")

    #def get_client_with_phone_number_xs(self, phone_number):
    #    return self.get_client_shop_with_phone_number(self.get_executor(), phone_number)

    #def get_executor(self):
    #    return self.shop

    def get_last_order_client(self, client):
        if Order.objects.filter(customer=client).count() > 1:
            print 'Error : Too many orderi get_last_order_client()', Order.objects.filter(customer=client).count()
        elif Order.objects.filter(customer=client).count() == 0:
            raise ValidationError(u"У клиента нет ни одного закзаза.")
        return Order.objects.filter(customer=client).order_by('-id')[0]

    #def get_last_order_for_client_with_phone_number_xs(self, phone_number):
    #    client = self.get_client_shop_with_phone_number(self.get_executor(), phone_number)
    #    return self.get_last_order_client(client)

    #def get_loyalty_xs(self):
    #    from eloyalty.models import ServiceRepositoryLoyalty
    #    srl = ServiceRepositoryLoyalty()
    #    loyalties = srl.list_loyalty_for_owner(self, self.get_executor())
    #    if len(loyalties) > 1:
    #        raise ValidationError(u"Error : Do not use size XS.")
    #    return loyalties[0]

    def get_shop_size(self):
        return self.shop.size

    #def get_my_order(self, order_id):
    #    #TODO проверка прав доступа к заказу.
    #    return Order.objects.get(id=order_id, seller=self)

    def get_order(self, order_id):
        #TODO проверка прав доступа к заказу.
        return Order.objects.get(id=order_id, seller=self)

    #def get_my_customer(self, customer_id):
    #    #TODO Нужна проверка прав доступа к заказу.
    #    return Shop.objects.get(id=customer_id)

    def get_customer(self, customer_id):
        #TODO Нужна проверка прав доступа к заказу.
        return Shop.objects.get(id=customer_id)

    #def get_pickup_point_xs(self):
    #    if self.pickup_points.all().count() > 1:
    #        raise ValidationError(u"Error : Do not use size XS.")
    #    return self.pickup_points.all()[0]

    def has_basket_for_client_in_shop(self, client, shop):
        for basket in Basket.objects.filter(customer=client, executor=shop):
            return True
        return False

    #def get_easy_product(self, product_id):
    #    #TODO Нужна проверка прав доступа к заказу.
    #    return Product.objects.get(id=product_id)

    def has_order(self, order_id):
        return True if Order.objects.filter(id=order_id, seller=self).count() > 0 else False

    def has_shop_client_with_phone_number(self, shop, phone_number):
        if not self.is_work_in_shop(shop):
            raise ValidationError(u"Выбранный прожавец не работает в указханном магазине.")
        for client in Shop.objects.filter(phone_number=phone_number): # не безопасно
            if self.has_shop_client(shop, client):
                return True
        return False

    def has_shop_client(self, shop, client):
        if self.is_work_in_shop(shop) and client in self.shop.clients.all():
            return True
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

    def is_work_in_shop(self, shop):
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

    def list_executor(self):
        return [self.shop]

    def list_loyalty(self, executor):
        from eloyalty.models import ServiceRepositoryLoyalty
        srl = ServiceRepositoryLoyalty()
        #loyalties = srl.list_loyalty_for_owner(self, self.get_executor())
        loyalties = srl.list_loyalty_for_owner(self, executor)
        return loyalties
        #if len(loyalties) > 1:
        #    raise ValidationError(u"Error : Do not use size XS.")
        #return loyalties[0]

    def list_order_for_shop(self, executor, pickup_point):
        return Order.objects.filter(executor=executor, pickup_point=pickup_point, seller=self)

    #def list_order_xs(self):
    #    executor = self.get_executor_xs()
    #    pickup_point = self.get_pickup_point_xs()
    #    return Order.objects.filter(executor=executor, pickup_point=pickup_point, seller=self)

    def list_product_in_stock(self, category):
        storages = self.shop.storages.all()
        products = set()
        for storage in storages:
            for product in storage.list_product():
                products.add(product)
        return list(products)

    #def list_easy_product(self):
    #    #TODO У каждого магазина должен быть свой набор продуктов или можно испоьзовать общий.
    #    # но не давать возможноть изменять никакой инфы по продуктам в базе, только создавать.
    #    # тогда будет общая база продуктов и в дальнейшем мапить не надо будет.
    #    products = []
    #    for product in Product.objects.all():
    #        if product.id != 1:
    #            products.append(product)
    #    return products

    def max_allow_ball_for_spend_for_order(self, order, purchaser, customer, executor, loyalty):
        datetime_for_check = None
        all_ball = loyalty.get_balance(None, customer, datetime_for_check)
        max_ball_for_spend = loyalty.create_range_ball(None, int(order.calculate_price_without_loyalty_balls()))[1]
        if max_ball_for_spend > all_ball:
            ball_for_spend = all_ball
        else:
            ball_for_spend = max_ball_for_spend
        return ball_for_spend

    def list_pickup_points(self, params_basket, client_city, client_type):
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

    #def process_order_with_ball_type_xs(self, order, customer, ball_type):
    #    pickup_point = self.get_pickup_point_xs()
    #    self.process_order_with_ball_type_s(order, customer, ball_type, pickup_point)

    #def process_order_with_ball_type_s(self, order, customer, ball_type, pickup_point):
    #    purchaser = Purchaser.objects.get(shop=customer)
    #    executor = self.get_executor()
    #    loyalty = self.get_loyalty_xs()
    #    if ball_type == 'MAX':
    #        ball_for_spend = self.__max_allow_ball_for_spend_for_order(order, purchaser, customer, executor, loyalty)
    #    elif ball_type == 'ZERO':
    #        ball_for_spend = 0
    #    self.process_order_without_customer_security(order, purchaser, customer, executor, loyalty, ball_for_spend, pickup_point)

    #def process_order_max_ball_xs(self, order, customer):
    #    purchaser = Purchaser.objects.get(shop=customer)
    #    executor = self.get_executor()
    #    loyalty = self.get_loyalty()
    #    pickup_point = self.get_pickup_point()
    #    ball_for_spend = self.__max_allow_ball_for_spend_for_order(order, purchaser, customer, executor, loyalty)
    #    self.process_order_without_customer_security(order, purchaser, customer, executor, loyalty, ball_for_spend, pickup_point)

    #def process_order_zero_ball_xs(self, order, customer):
    #    purchaser = Purchaser.objects.get(shop=customer)
    #    executor = self.get_executor()
    #    loyalty = self.get_loyalty()
    #    pickup_point = self.get_pickup_point()
    #    ball_for_spend = 0
    #    self.process_order_without_customer_security(order, purchaser, customer, executor, loyalty, ball_for_spend, pickup_point)

    #def process_order_easy_with_max_allow_ball_without_customer_security(self, order, customer, executor, loyalty, pickup_point):
    #    purchaser = Purchaser.objects.get(shop=customer)
    #    self.process_order_with_max_allow_ball_without_customer_security(order, purchaser, customer, executor, loyalty, pickup_point)

    #def process_order_easy_with_zero_ball_without_customer_security(self, order, customer, executor, loyalty, pickup_point):
    #    ball = 0
    #    purchaser = Purchaser.objects.get(shop=customer)
    #    self.process_order_without_customer_security(order, purchaser, customer, executor, loyalty, ball, pickup_point)

    #def process_order_with_max_allow_ball_without_customer_security(self, order, purchaser, customer, executor, loyalty, pickup_point):
    #    ball_for_spend = self.__max_allow_ball_for_spend_for_order(order, purchaser, customer, executor, loyalty)
    #    self.process_order_without_customer_security(order, purchaser, customer, executor, loyalty, ball_for_spend, pickup_point)

    def process_order_without_customer_security(self, order, purchaser, customer, executor, loyalty, ball_for_spend, pickup_point):
        # actor - аккаунт для purchaser
        # purchaser - закупщик у какогото ЮР Лица. (customer, executor, ...)
        # shop - executor
        # client - customer

        if ball_for_spend:
            self.__spend_customer_ball_for_order(order, purchaser, customer, executor, loyalty, ball_for_spend)
        else:
            #purchaser.pay_ball(order, 0)
            order.loyalty_ball = 0
            order.save()

        # Нужно для провери что пришла оплата тоглда можно начислять балы за покупку.
        #self.create_price_last_order()
        #link_for_payment = self.create_payemnt_link_for_last_order()
        if not self.check_payment_for_last_order():
            return None

        self.__accumulate_customer_ball_for_order(order, purchaser, customer, executor, loyalty)

        #self.__change_status_for_last_order(u'Ожидает выдачи позиций заказа клиенту')
        self.__change_status_for_order(order, u'Ожидает выдачи позиций заказа клиенту')

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

    def list_pickup_point(self):
        return self.pickup_points.all()

    def list_shop(self):
        #return [self.shop]
        return self.pickup_points.all()

    def __spend_customer_ball_for_order(self, order, purchaser, customer, executor, loyalty, ball_for_spend):
        datetime_for_check = None
        all_ball = loyalty.get_balance(purchaser, customer, datetime_for_check)
        if ball_for_spend > all_ball:
            ball_for_spend = all_ball

        available_day = 0
        #loyalty.transfer_ball(seller, customer, executor, ball_for_spend, available_day)
        loyalty.transfer_ball(purchaser, customer, executor, ball_for_spend, available_day)

        #purchaser.pay_ball(order, ball_for_spend)
        order.loyalty_ball = ball_for_spend
        order.save()

        self.__change_status_for_order(order, u'Оплатил часть заказа балами')

    def __unicode__(self):
        return u"Seller (%s) : %s [shop : %s]" % (self.id, self.title, self.shop)


#class Customer(object):
#    """
#    Используется в системе лояльности для связывания клиента и счета
#    """
#    def set_payment_balls_for_last_order(self, balls):
#        pass
#
#    def pay_by(self, link_for_payment):
#        pass

class Basket(models.Model):
    customer = models.ForeignKey(Shop, related_name='customer_shop')
    executor = models.ForeignKey(Shop, related_name='executor_shop')
    purchaser = models.ForeignKey(Purchaser)
    seller = models.ForeignKey(Seller)

    def add(self, product, quantity, price, currency):
        """
        При наличии такого продукта в корзине пол тойже ценет и в той же валюте - нужно увеличить quantity
        баскет уже должен быть сохранен(иметь id)
        """
        print 'Error : Nead fix.'
        basket_element = BasketElement(basket=self, product=product, quantity=quantity, price=price, currency=currency)
        basket_element.save()

    def elements(self):
        return list(BasketElement.objects.filter(basket=self))

class BasketElement(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(u"Цена")
    price = models.DecimalField(u"стоимость продажи одной штуки", decimal_places=2, max_digits=7)
    currency = models.CharField(u"Валюта", max_length=5)
    basket = models.ForeignKey(Basket)

class Order(models.Model):
    customer = models.ForeignKey(Shop, related_name='order_customer_shop')
    executor = models.ForeignKey(Shop, related_name='order_executor_shop')
    purchaser = models.ForeignKey(Purchaser)
    seller = models.ForeignKey(Seller)

    create_datetime = models.DateTimeField(u'дата и время создание заказа', auto_now_add=True)
    pickup_point = models.ForeignKey(PickupPoint)
    pickup_dateteme = models.DateTimeField(u'дата и время вручения всего заказа(т.е. последней партии)', auto_now_add=True)

    loyalty_ball = models.IntegerField(u"Оплаено балами.", null=True, blank=True)
    rewards_ball = models.IntegerField(u"Накопленно балов.", null=True, blank=True)

    def add(self, product, quantity, price, currency):
        """
        При наличии такого продукта в корзине пол тойже ценет и в той же валюте - нужно увеличить quantity
        баскет уже должен быть сохранен(иметь id)
        """
        print 'Error : Nead fix.'
        print '+++++', product, quantity, price, currency
        order_element = OrderElement(order=self, product=product, quantity=quantity, price=price, currency=currency)
        order_element.save()

    def calculate_price(self):
        #price = 0
        #for order_element in OrderElement.objects.filter(order=self):
        #    price += order_element.quantity * order_element.price
        price = self.calculate_price_without_loyalty_balls()
        if self.loyalty_ball:
            price -= self.loyalty_ball
        if price < 0:
            raise ValidationError(u"Стоимоть не может быть отрицательной!")
        return price

    def calculate_price_without_loyalty_balls(self):
        price = 0
        for order_element in OrderElement.objects.filter(order=self):
            price += order_element.quantity * order_element.price
        return price

    def delete_easy_products(self):
        for e in OrderElement.objects.filter(order=self):
            if e.product.id != 1:
                e.delete()

    def list_easy_product(self):
        products = []
        for e in OrderElement.objects.filter(order=self):
            if e.product.id != 1:
                products.append(e.product)
        return products

    @classmethod
    def list_order(cls, order_specification):
        return Order.objects.filter(
            executor=order_specification.executor,
            pickup_point__in=order_specification.pickup_points,
            seller=order_specification.seller)

    def __unicode__(self):
        return u"Order (%s) : %s %s %s %s" % (self.id, self.purchaser, self.customer, self.executor, self.seller)

class OrderElement(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(u"Цена")
    price = models.DecimalField(u"стоимость продажи одной штуки", decimal_places=2, max_digits=7)
    currency = models.CharField(u"Валюта", max_length=5)
    order = models.ForeignKey(Order)

class OrderSpecification(object):
    def __init__(self):
        self.pickup_point_specification = None
        self.pickup_points = []
        self.executor = None
        self.seller = None
