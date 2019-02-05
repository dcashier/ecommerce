#!-*-coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render

from eactor.models import AuthSystem

from django.template import RequestContext, loader

class MyView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'dcashier/static/index.html')
        #return render(request, 'static/index.html')
        #return HttpResponse('Hello, enother World!')

def index(request):

    answer = {}
    if request.session.get('actor_id'):
        auth_system = AuthSystem()
        actor = auth_system.get_actor_by_id(request.session.get('actor_id'))
        answer['actor'] = actor
        answer['is_login'] = True
        if request.session.get('shop_id'):
            shop_id = request.session.get('shop_id')
            actor = get_actor_for_request_if_login(request)
            shops = actor.shops()
            for shop in shops:
                if str(shop.id) == str(shop_id):
                    answer['shop'] = shop
                    break
            if request.session.get('order_id'):
                answer['is_order'] = True
    else:
        answer['is_login'] = False

    template = loader.get_template('dcashier/static/index.html')
    context = RequestContext(request, answer)
    #return HttpResponse(template.render(context))
    return HttpResponse(template.render(context.flatten()))

class ActorNone(object):
    def shops(self):
        return []

class ShopNone(object):
    pass

class AuthPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dcashier/static/authPage.html')

def get_actor_for_request_if_login(request):
    if request.session.get('actor_id'):
        auth_system = AuthSystem()
        actor = auth_system.get_actor_by_id(request.session.get('actor_id'))
        return actor
    return ActorNone()

def get_shop_for_request_if_login(request):
    actor = get_actor_for_request_if_login(request)
    if actor:
        shop_id = request.session.get('shop_id')
        if shop_id:
            shops = actor.shops()
            for shop in shops:
                if str(shop.id) == str(shop_id):
                    return shop
    return ShopNone()

class Login(View):
    def post(self, request, *args, **kwargs):
        phone_number = request.POST['authNameInput']
        password = request.POST['authPasswordInput']

        auth_system = AuthSystem()
        if auth_system.has_actor_by_phone_numnber_password(phone_number, password):
            actor = auth_system.get_actor_by_phone_numnber_password(phone_number, password)
            request.session['actor_id'] = actor.id
            return HttpResponse("You're logged in. <a href=\"/\">main</a>")
	else:
            return HttpResponse("Your username and password didn't match. <a href=\"/\">main</a>")

class Logout(View):
    def post(self, request, *args, **kwargs):
        try:
            del request.session['actor_id']
        except KeyError:
            pass
        return HttpResponse("You're logged out. <a href=\"/\">main</a>")

class SelectShopPage(View):
    def get(self, request, *args, **kwargs):
        actor = get_actor_for_request_if_login(request)
        shops = actor.shops()

        answer = {}
        answer['shops'] = shops
        template = loader.get_template('dcashier/static/selectShopPage.html')
        context = RequestContext(request, answer)
        #return HttpResponse(template.render(context))
        return HttpResponse(template.render(context.flatten()))

    def post(self, request, *args, **kwargs):
        shop_id = request.POST['shop_id']
        actor = get_actor_for_request_if_login(request)
        shops = actor.shops()
        for shop in shops:
            if str(shop.id) == str(shop_id):
                request.session['shop_id'] = shop_id
                return HttpResponse("You're select shop!")
        return HttpResponse("You're select not good shop")

class ShopPage(View):
    def get(self, request, *args, **kwargs):
        actor = get_actor_for_request_if_login(request)
        shop = get_shop_for_request_if_login(request)
        #seller = actor.seller()
        #clent = get_client_by_phone(request.POST['phone_number'])
        #order = seller.create_order([get_default_product], clent)

        answer = {}
        answer['shop'] = shop
        template = loader.get_template('dcashier/static/shopPage.html')
        context = RequestContext(request, answer)
        #return HttpResponse(template.render(context))
        return HttpResponse(template.render(context.flatten()))


    def post(self, request, *args, **kwargs):
        actor = get_actor_for_request_if_login(request)
        shop = get_shop_for_request_if_login(request)

        client_phone_number = request.POST['customerPhoneInput']
        order_sum = request.POST['dealSummInput']

        seller = actor.seller
        if not seller.has_shop_client_with_phone_number(shop, client_phone_number):
            seller.create_client_shop_with_phone_number(shop, client_phone_number)
        client = seller.get_client_shop_with_phone_number(shop, client_phone_number)

        from eproduct.models import Product
        from decimal import Decimal
        default_product = Product.objects.get(id=1)
        quantity = 1
        price = Decimal(order_sum)
        currency = "RUS"

        from eseller.models import Purchaser
        purchaser = Purchaser.get_purchaser_with_phone_number_for_client(client_phone_number, client)
        #print client, shop
        if not seller.has_basket_for_client_in_shop(client, shop):
            #print purchaser, actor, purchaser == actor
            seller.create_basket_for_client_in_shop(client, shop, purchaser)
        basket_client = seller.get_basket_for_client_in_shop(client, shop)
        seller.add_product_in_basket(basket_client, default_product, quantity, price, currency)

        from estorage.models import PickupPoint
        pickup_point = PickupPoint.objects.get(id=1)

        seller.create_order_from_busket_and_pickup_point(client, shop, purchaser, basket_client, pickup_point)
        order_client = seller.get_last_order_client(client)
        request.session['order_id'] = order_client.id
        request.session['client_id'] = client.id
        request.session['purchaser_id'] = purchaser.id

        basket_client.delete()

        #ball = 1
        #purchaser.pay_ball(order_client, ball)
        #self.assertEqual(Decimal('4.00'), order_client.calculate_price())

#        get_client
#        order = Order()
        return HttpResponse("You're create <a href=\"/newDealPage.html\">order</a>" )


class NewDealPage(View):
    def get(self, request, *args, **kwargs):
        actor = get_actor_for_request_if_login(request)
        shop = get_shop_for_request_if_login(request)
        seller = actor.seller
        from eseller.models import Order
        order = Order.objects.filter(id=request.session.get('order_id'))[0]
        from eshop.models import Shop
        client = Shop.objects.filter(id=request.session.get('client_id'))[0]
        from eloyalty.models import ServiceRepositoryLoyalty
        srl = ServiceRepositoryLoyalty()
        loyalties = srl.list_loyalty_for_owner(seller, shop)
        loyalty = loyalties[0]

        if not loyalty.is_registration(seller, client):
            loyalty.register_in_loyalty_hello_0(seller, client, shop)

        datetime_for_check = None
        all_ball = loyalty.get_balance(actor, client, datetime_for_check)

        #reward_ball = seller.calculate_revards_balls_for_last_order()
        max_ball_for_pay = loyalty.create_range_ball(actor, int(order.calculate_price()))[1]
        if max_ball_for_pay > all_ball:
            max_ball_for_pay = all_ball

        answer = {}
        answer['order_sum'] = int(order.calculate_price())
        answer['client'] = client
        answer['all_ball'] = all_ball
        #answer['reward_ball'] = max_ball_for_pay
        answer['max_ball_for_pay'] = max_ball_for_pay
        answer['max_percent_in_loyalty'] = loyalty.get_max_percent()
        answer['order_sum_with_ball'] = int(order.calculate_price()) - max_ball_for_pay
        template = loader.get_template('dcashier/static/newDealPage.html')
        context = RequestContext(request, answer)
        #return HttpResponse(template.render(context))
        return HttpResponse(template.render(context.flatten()))


    def post(self, request, *args, **kwargs):
        actor = get_actor_for_request_if_login(request)
        shop = get_shop_for_request_if_login(request)
        seller = actor.seller
        from eseller.models import Order
        order = Order.objects.filter(id=request.session.get('order_id'))[0]
        from eshop.models import Shop
        client = Shop.objects.filter(id=request.session.get('client_id'))[0]
        from eloyalty.models import ServiceRepositoryLoyalty
        srl = ServiceRepositoryLoyalty()
        loyalties = srl.list_loyalty_for_owner(seller, shop)
        loyalty = loyalties[0]
        datetime_for_check = None
        all_ball = loyalty.get_balance(actor, client, datetime_for_check)

        print request.POST['action']  == 'write_off', request.POST['action']
        if request.POST['action']  == 'write_off':
            max_ball_for_pay = loyalty.create_range_ball(actor, int(order.calculate_price()))[1]
            if max_ball_for_pay > all_ball:
                max_ball_for_pay = all_ball
            from eseller.models import Purchaser
            purchaser = Purchaser.objects.get(id=request.session.get('purchaser_id'))
            purchaser.pay_ball(order, max_ball_for_pay)
            available_day = 0
            loyalty.transfer_ball(seller, client, shop, max_ball_for_pay, available_day)

        elif request.POST['action']  == 'save_up':
            pass

        seller.create_price_last_order()
        link_for_payment = seller.create_payemnt_link_for_last_order()

        if not seller.check_payment_for_last_order():
            return None

        reward_ball = seller.calculate_revards_balls_for_last_order()
        available_day = 90
        loyalty.transfer_ball(seller, shop, client, reward_ball, available_day)

        seller.change_status_for_last_order(u'Ожидает выдачи позиций заказа клиенту')

        return HttpResponse("You're create order pay : %s, save up %s ball's" % (order.calculate_price(), reward_ball))
