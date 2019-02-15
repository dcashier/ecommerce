#!-*-coding: utf-8 -*-
from django.test import TestCase

from eloyalty.models import *
from django.test.client import Client
import json
import sys
import time
import pprint
from decimal import Decimal
#import datetime

# надо потом попробовать от этого избавиться
from eseller.models import *

class TestELoyalty(TestCase):
    def setUp(self):
        print "SETUP DATA FOR TestELoyalty..."
        self.assertEqual.__self__.maxDiff = None

    def test_seller(self):
        """
        Кто создатель системы лояльности?
            Один конкретный магазин или нет?
            Можно завести менеджера системы лояльности, который будет создавать системы, и видеть только свои системы.
                А магазины будут приходить к этому менеджеру и говорить что они хотят свой магазин подключить к данной системе.

        Система лояльности это часть магазина и рабоатет только в рамках одного магазина или
            несколько магахинов могут быть объеденены в рамках одной системы(можно делать так но с проверкой что только один рабочий).
                Также как один магазин может быть представлен в нескольких системах лояльности.
                    Как сделать так чтобы магазин не видел других систем а только свои или в которых участвует.
        У системы лояльности те же клиенты что и у магазина или свои?
            Допустим каждый клиент должен знать свой данные в кажом приложении.

        Вова хочет платить меньше. А продавец хочет чтобы покупательи приходили к нему постоянно и не ходили на сторону.
        Поэтому сделали систему лояльности.
        Чтобы Вове платить меньше надо постоянно покупать(получать балы поставщика),
            у опеределенного поставщика чтобы потом же у него расплачиваться балами.

        Ритейлер создает инстанс сисстемы лояльности.
        Вове узнает у ритейера какие есть системы. Или приложение всегда содерит только одну систему для магазина выпустившего приложение.
        Далее или Вова сам через сайт/приложение/телеграм регестириуется в системе лояльности.
            Или кассир в магазине регестирует номер телефона Вовы и начисляет ему баллы.
                Для списывания балов Вове нужно будет предьявить телефон с кодом СМС на текущую попкупку чтобы спсиать балы.
                Или онлай связать номер телефона с его аккаунтом
                    Т.е. можно разаделить аккаунт в системе лояльности и счет привязанныйк телефону.
                        Хотя проще для реализации не давать связывать номер с аккаунтом, а разрешать это только при создании.
                            Чтобы не писать сложной синхронизации и склейки двух аккаунтов на первом этапе.
        Следующее действие Вове надо наать копить балы.
            Один из способов делать покупки в магазине.
        Вова приходит в магазин делает покупку и получает балы.
            Владелец магазина создает правила рассчета начислений. Можно на своей стороне. Можно на стороне системы лояльности. Можно в брокере рассчетов начислений.
            Пока сделаем это настороне магазина, и очень простой подход который берет 10 % от стоимости заказа.

        Онлайн покупка. Сейча рассматриваем случай подтверждения через интенрет!
            Продавец(один из акаунтов магазина) считал QR код(с одного из акаунта смартфона клиента) и смог идентифицировать клиента.
            Магазин(продавец с аккаунта в память-сессию которого он считал номер клиента) создает инцидент заказ клиента
                в рамках заказа отправляется запрос клиенту сколько списать балов?
                клиент открывает видет новый не закрытый заказ входи в него, указываетс сумму в баллах сколько списать(определеные пределы - к примеру не боллее 50% от заказа)
                магазин(продавец видит что один из его заказов сменил статус) получает подтверждение.
            Магазин(продавец) после получения балов от клиента фиксирует итоговую сумму "заказа с балами"
            Выдает(продавец) клиенту ссылку на онлайн оплату.
                банк после оплаты перенаправляет клиента на страницу сайта магазина где все хорошо.
            Магазин ждет подтверждения от банка.
            Когда пришло подтверждение клиенту или сразу(или через 2 недели чтобы не был совершен возврат) начисляются балы
            Все.
        """

        shop_1 = Shop()
        shop_1.save()

        #seller_shop_1 = None
        seller_shop_1 = Seller(shop=shop_1)
	seller_shop_1.save()

	srl = ServiceRepositoryLoyalty()

        # пока у репозитория спрашивает сам магазин
        self.assertEqual(0, len(srl.list_loyalty_for_owner(seller_shop_1, shop_1)))

        self.assertFalse(srl.has_loyalty_for_owner(seller_shop_1, shop_1))
        title = "Roga i Kopita"
        max_percent = 50
        start_ball = 1000000
        start_ball_available_day = 20000
        reward_percent = 10
        available_day =90
        is_need_auth = True
        srl.create_loyalty(seller_shop_1, shop_1, title, max_percent, start_ball, start_ball_available_day, reward_percent, available_day, is_need_auth)

        #loyalty = executor.get_loyalty()
        loyalties = srl.list_loyalty_for_owner(seller_shop_1, shop_1)
        self.assertEqual(1, len(loyalties))
        loyalty_1 = loyalties[0]
        self.assertEqual(title, loyalty_1.get_title())

        ##create_loyalty(cls, actor, executor, title, max_percent, start_ball, start_ball_available_day, reward_percent, available_day, is_need_auth):
        #start_ball = 1000000
        #loyalty_record = LoyaltyRecord(title="Roga i Kopita 2", max_percent=50, start_ball=start_ball, owner=shop_1, is_need_auth=True)
        #loyalty_record.save()
        #loyalty_2 = Loyalty(loyalty_record)

        #reward_percent = 10
        #available_day = 90
        #start_ball_available_day = 30
        #loyalty_2.register_in_loyalty_executor(shop_1, reward_percent, available_day, start_ball, start_ball_available_day)

        client_1 = Shop()
        client_1.save()

        self.assertFalse(loyalty_1.is_registration(seller_shop_1, client_1))
        loyalty_1.register_in_loyalty_hello_1000(seller_shop_1, client_1, shop_1)
        self.assertTrue(loyalty_1.is_registration(seller_shop_1, client_1))


        # Сейчас будет работать представитель клиента
        #actor_client_new = Customer()
        actor_client_new = None

        #client_2 = Shop()
        #client_2.save()
        #actor_client_2 = None

        #self.assertFalse(loyalty_1.is_registration(actor_client_2, client_2))
        #loyalty_1.register_in_loyalty_hello_1000(actor_client_2, shop_1, client_2)
        #self.assertTrue(loyalty_1.is_registration(actor_client_2, client_2))

        params = {
            'fio': u'Ануфрева Авдотья Тимофеевна',
            'birthday': u'1933-10-06',
            'phone_number': u'89136581258',
            'phone_m_type': u'rus',
        }
        is_person = True
        self.assertFalse(Shop.objects.filter(phone_number=params['phone_number'], is_person=is_person).count() > 0)

        client_new = Shop()
        client_new.title = params.get('title')
        client_new.is_person=is_person
        client_new.fio = params.get('fio')
        client_new.birthday = params.get('birthday')
        client_new.phone_number = params.get('phone_number')
        client_new.phone_m_type = params.get('phone_m_type')
        client_new.save()

        #seller_shop_1.create_customer_shop_with_phone_number(shop_1, client_new['phone_number'])
        purchaser = Purchaser(
            title=u"Default purchaser when Seller create Client.",
            shop=client_new,
            phone_number=client_new.phone_number)
        purchaser.save()

        ## надо вынести
        #link = EntityLinkActor()
        #link.entity = record
        #link.actor = actor.get_record()
        #link.save()

        clients = Shop.objects.filter(phone_number=params['phone_number'], is_person=is_person)
        self.assertFalse(len(clients) > 1)
        self.assertFalse(len(clients) < 1)
        self.assertTrue(len(clients) == 1)
        client_2 = clients[0]

        self.assertEqual(client_new, client_2)

        self.assertFalse(loyalty_1.is_registration(actor_client_new, client_2))
        loyalty_1.register_in_loyalty_hello_0(actor_client_new, client_2, shop_1)
        self.assertTrue(loyalty_1.is_registration(actor_client_new, client_2))

        params = {
            'phone_number': u'89136581258',
            'phone_m_type': u'rus',
        }
        #customer_list = actor_executor.find_customer_by_params_in_loyalty(
        #    executor,
        #    params,
        #    loyalty_executor,
        #)
        #customer = customer_list[0]

        #find_customer_by_params(self, executor, params):
        clients = []
        if params.get('phone_number') and params.get('phone_m_type'):
            for client in Shop.objects.filter(phone_number=params['phone_number'], phone_m_type=params['phone_m_type']):
                clients.append(client)
        else:
            for entity in Shop.objects.all():
                clients.append(client)
        self.assertEqual(1, len(clients))
        for client in clients:
            self.assertTrue(loyalty_1.is_registration(shop_1, client))

        # Создаем заказ
        brand_xiaomy = Brand(title="Xiaomy")
        brand_xiaomy.save()
        product_mi8 = Product(title='Mi 8', brand=brand_xiaomy)
        product_mi8.save()
        region_center = Region(title=u"Центральный")
        region_center.save()
        city_moscow = City(title=u"Moscow", region=region_center)
        city_moscow.save()
        pickup_point_1 = PickupPoint(title=u"pickup 1", city=city_moscow)
        pickup_point_1.save()
        interval = [datetime.datetime(2000, 01, 01, 12, 30, 00), datetime.datetime(2000, 01, 01, 20, 00, 00)]
        order_params = {
            'version': 'v1',
            'basket': [
                {
                    'product': product_mi8,
                    'quantity': 1,
                    'price': Decimal('115.61'),
                    'currency': "USD",
                },
            ],
            'pickup': {
                'point': pickup_point_1,
                'interval': interval,
            },
            'seller': None,
            'client': None,

            'shop': shop_1,
            'client': client_2,
            'payment_balls': None,
            'status': ['create'],
        }
        #seller_shop_1.create_order(order_params)
        self.assertFalse(seller_shop_1.has_basket_spec_customer_executor(client_2, shop_1))
        purchaser = Purchaser.get_purchaser_with_phone_number_for_client(client_2.phone_number, client_2)
        seller_shop_1.create_basket_for_client_in_shop(client_2, shop_1, purchaser)
        self.assertTrue(seller_shop_1.has_basket_spec_customer_executor(client_2, shop_1))
        basket_client = seller_shop_1.get_basket_spec_executor_customer(client_2, shop_1)
        seller_shop_1.add_product_in_basket(basket_client, product_mi8, 1, Decimal('115.61'), 'USD')
        seller_shop_1.create_order_from_busket_and_pickup_point(client_2, shop_1, purchaser, basket_client, pickup_point_1)
        basket_client.delete()

        # так как Вова только зарегился у него 0 балов.
        vava_has_balls = 0
        datetime_for_check = None
        self.assertEqual(vava_has_balls, loyalty_1.get_balance(actor_client_new, client_2, datetime_for_check))

        vava_want_spend_balls = 0
        available_day = 0
        #actor_client_new.set_payment_balls_for_last_order(vava_want_spend_balls)
        #loyalty_1.transfer_ball(seller_shop_1, client_1, shop_1, vava_want_spend_balls, available_day)

        #seller_shop_1.create_price_last_order()

        #link_for_payment = seller_shop_1.create_payemnt_link_for_last_order()

        #actor_client_new.pay_by(link_for_payment)

        self.assertTrue(seller_shop_1.check_payment_for_last_order())


        #reward_balls = seller_shop_1.calculate_rewards_balls_for_last_order(loyalty_1, client_2)
        last_order_for_client_2 = seller_shop_1.get_last_order_spec_customer(client_2)
        reward_balls = seller_shop_1.get_rewards_balls_for_order(last_order_for_client_2, loyalty_1)
        #self.assertEqual(3000, reward_balls)
        #self.assertEqual(57, reward_balls)
        self.assertEqual(Decimal('11.561'), reward_balls)
        #actor_executor.confirm_out_payment_for_loyalty(shop_1, client_1, loyalty_1, 3000, 90)
        available_day = 90
        loyalty_1.transfer_ball(seller_shop_1, shop_1, client_2, reward_balls, available_day)

        # seller_shop_1.change_status_for_last_order(u'Ожидает выдачи позиций заказа клиенту')
        # на этом первая покупка Вовы закончилась.


        ####


        # Проведем еще одну закоупку теперь чать ее Вава оплатит балами.

	srl = ServiceRepositoryLoyalty()
        shop_1
	seller_shop_1 = None
        seller_shop_2 = Seller(shop=shop_1)
	seller_shop_2.save()


        loyalties = srl.list_loyalty_for_owner(seller_shop_2, shop_1)
        loyalty_1 = loyalties[0]

        #actor_client_new = Customer()
        actor_client_new = None 
        params = {
            #'fio': u'Ануфрева Авдотья Тимофеевна',
            #'birthday': u'1933-10-06',
            'phone_number': u'89136581258',
            #'phone_m_type': u'rus',
        }
        clients = Shop.objects.filter(phone_number=params['phone_number'], is_person=is_person)
        client_2 = clients[0]

        product_mi8
        pickup_point_1
        interval = [datetime.datetime(2000, 01, 01, 12, 30, 00), datetime.datetime(2000, 01, 01, 20, 00, 00)]
        order_params = {
            'version': 'v1',
            'basket': [
                {
                    'product': product_mi8,
                    'quantity': 1,
                    'price': Decimal('130'),
                    'currency': "USD",
                },
            ],
            'pickup': {
                'point': pickup_point_1,
                'interval': interval,
            },
            'seller': None,
            'client': None,

            'shop': shop_1,
            'client': client_2,
            'payment_balls': None,
            'status': ['create'],
        }
        #seller_shop_2.create_order(order_params)
        self.assertFalse(seller_shop_2.has_basket_spec_customer_executor(client_2, shop_1))
        purchaser = Purchaser.get_purchaser_with_phone_number_for_client(client_2.phone_number, client_2)
        seller_shop_2.create_basket_for_client_in_shop(client_2, shop_1, purchaser)
        self.assertTrue(seller_shop_2.has_basket_spec_customer_executor(client_2, shop_1))
        basket_client = seller_shop_2.get_basket_spec_executor_customer(client_2, shop_1)
        seller_shop_2.add_product_in_basket(basket_client, product_mi8, 1, Decimal('130'), 'USD')
        seller_shop_2.create_order_from_busket_and_pickup_point(client_2, shop_1, purchaser, basket_client, pickup_point_1)

        # так как Вова не только зарегился, и у него в системе уже есть балы.
        #vava_has_balls = 3000
        #vava_has_balls = 57
        vava_has_balls = 11
        datetime_for_check = None
        self.assertEqual(vava_has_balls, loyalty_1.get_balance(actor_client_new, client_2, datetime_for_check))

        #vava_want_spend_balls = 2000
        #vava_want_spend_balls = 50
        vava_want_spend_balls = 5
        available_day = 0
        #actor_client_new.set_payment_balls_for_last_order(vava_want_spend_balls)
        loyalty_1.transfer_ball(seller_shop_2, client_2, shop_1, vava_want_spend_balls, available_day)
        #self.assertEqual(1000, loyalty_1.get_balance(actor_client_new, client_2, datetime_for_check))
        #self.assertEqual(7, loyalty_1.get_balance(actor_client_new, client_2, datetime_for_check))
        self.assertEqual(6, loyalty_1.get_balance(actor_client_new, client_2, datetime_for_check))

        #seller_shop_2.create_price_last_order()

        #link_for_payment = seller_shop_2.create_payemnt_link_for_last_order()

        #actor_client_new.pay_by(link_for_payment)

        self.assertTrue(seller_shop_2.check_payment_for_last_order())

        #reward_balls = seller_shop_2.calculate_rewards_balls_for_last_order(loyalty_1, client_2)
        last_order_for_client_2 = seller_shop_2.get_last_order_spec_customer(client_2)
        reward_balls = seller_shop_2.get_rewards_balls_for_order(last_order_for_client_2, loyalty_1)
        #self.assertEqual(65, reward_balls)
        self.assertEqual(Decimal('13.00'), reward_balls)
        #actor_executor.confirm_out_payment_for_loyalty(shop_1, client_1, loyalty_1, 3000, 90)
        available_day = 90
        loyalty_1.transfer_ball(seller_shop_2, shop_1, client_2, reward_balls, available_day)

        #self.assertEqual(72, loyalty_1.get_balance(actor_client_new, client_2, datetime_for_check))
        self.assertEqual(19, loyalty_1.get_balance(actor_client_new, client_2, datetime_for_check))
        #seller_shop_2.change_status_for_last_order(u'Ожидает выдачи позиций заказа клиенту')
        # на этом вторая покупка Вовы закончилась.



