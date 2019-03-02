#!-*-coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render
from eactor.models import AuthSystem
from django.template import RequestContext, loader
from django.shortcuts import redirect

from decimal import Decimal

class MyView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dcashier/static/index.html')

class Index(View):
    def get(self, request, *args, **kwargs):
        answer = {}
        if request.session.get('actor_id'):
            auth_system = AuthSystem()
            actor = auth_system.get_actor_by_id(request.session.get('actor_id'))
            answer['actor'] = actor
            answer['is_login'] = True
            if request.session.get('shop_id'):
                shop_id = request.session.get('shop_id')
                actor = get_actor_for_request_if_login(request)
                seller = actor.get_seller()
                shops = seller.list_shop()
                for shop in shops:
                    if str(shop.id) == str(shop_id):
                        answer['shop'] = shop
                        break
                if request.session.get('order_id'):
                    answer['is_order'] = True
        else:
            answer['is_login'] = False

        if request.session.get('price_last_order') and \
            request.session.get('reward_ball_last_order'):
            answer['price_last_order'] = int(request.session['price_last_order'])
            answer['reward_ball_last_order'] = int(request.session['reward_ball_last_order'])
            del request.session['price_last_order']
            del request.session['reward_ball_last_order']
        template = loader.get_template('dcashier/static/index.html')
        context = RequestContext(request, answer)
        return HttpResponse(template.render(context.flatten()))

class ActorNone(object):
    seller = None

    def get_seller(self):
        return None

    def is_null(self):
        return True

    def list_shop(self):
        return []

    def shops(self):
        return []

    def seller(self):
        return None

class ShopNone(object):
    def is_null(self):
        return True

class AuthPage(View):
    def get(self, request, *args, **kwargs):
        answer = {}
        answer['is_error_login'] = request.session.get('is_error_login')
        template = loader.get_template('dcashier/static/authPage.html')
        context = RequestContext(request, answer)
        return HttpResponse(template.render(context.flatten()))

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
            seller = actor.get_seller()
            shops = seller.list_shop()
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
            request.session['is_error_login'] = False
            return redirect('/')
            pass
        else:
            pass
            request.session['is_error_login'] = True
            return redirect('/authPage.html')

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
        if not request.session.get('actor_id'):
            return redirect('/')
        seller = actor.get_seller()
        shops = seller.list_shop()
        answer = {}
        answer['shops'] = shops
        template = loader.get_template('dcashier/static/selectShopPage.html')
        context = RequestContext(request, answer)
        return HttpResponse(template.render(context.flatten()))

    def post(self, request, *args, **kwargs):
        shop_id = request.POST['shop_id']
        actor = get_actor_for_request_if_login(request)
        seller = actor.get_seller()
        shops = seller.list_shop()
        for shop in shops:
            if str(shop.id) == str(shop_id):
                request.session['shop_id'] = shop_id
                return redirect('/')
        return redirect('/selectShopPage.html')

class SellerDealPage(View):
    def get(self, request, *args, **kwargs):
        if not request.session.get('actor_id'):
            return redirect('/')
        actor = get_actor_for_request_if_login(request)
        seller = actor.get_seller()
        executor = seller.get_executor()
        if not request.session.get('shop_id'):
            return redirect('/')
        shop = get_shop_for_request_if_login(request)
        if shop.is_null():
            return redirect('/')
        answer = {}
        answer['orders'] = seller.list_order()
        answer['seller'] = seller.get_object()
        answer['executor'] = executor
        answer['shop'] = shop
        answer['actor'] = actor
        template = loader.get_template('dcashier/static/sellerDealPage.html')
        context = RequestContext(request, answer)
        return HttpResponse(template.render(context.flatten()))

class ShopPage(View):
    def get(self, request, *args, **kwargs):
        actor = get_actor_for_request_if_login(request)
        shop = get_shop_for_request_if_login(request)
        answer = {}
        answer['shop'] = shop
        template = loader.get_template('dcashier/static/shopPage.html')
        context = RequestContext(request, answer)
        return HttpResponse(template.render(context.flatten()))

    def post(self, request, *args, **kwargs):
        actor = get_actor_for_request_if_login(request)
        seller = actor.get_seller()
        phone_number = request.POST['customerPhoneInput']
        order_sum = request.POST['dealSummInput']
        price = Decimal(order_sum)
        if seller.get_executor().is_size_xs():
            seller.create_order(phone_number, price)
        elif seller.get_executor().is_size_s():
            pickup_point = seller.get_pickup_point_spec_id(int(request.session.get('shop_id')))
            seller.create_order(phone_number, price, pickup_point)
        else:
            assert False
        #order = seller.get_last_order_for_client_with_phone_number(phone_number)
        client = seller.get_customer_spec_phone_number(phone_number)
        order = seller.get_last_order_spec_customer(client)
        request.session['order_id'] = order.id
        request.session['client_id'] = client.id
        return redirect('/newDealPage.html')

class NewDealPage(View):
    def get(self, request, *args, **kwargs):
        """
        Продавец запрашивает информацию по сделке.
        Может вызывть только методы у объекта продавец(т.е. только у самого себе - отдавать приказы только себе и подчиненным).
        """
        actor = get_actor_for_request_if_login(request)
        shop = get_shop_for_request_if_login(request)
        if shop.is_null():
            return redirect('/')
        seller = actor.get_seller()
        executor = seller.get_executor()
        if not request.session.get('order_id'):
            return redirect('/')
        if not seller.has_order_spec_id(request.session.get('order_id')):
            return redirect('/')
        order = seller.get_order_spec_id(request.session.get('order_id'))
        client = seller.get_customer_spec_id(request.session.get('client_id'))

        if not seller.is_registration_in_loyalty(client):
            seller.registration_in_loyalty(client)

        all_ball = seller.get_balance_customer_in_loyalty(client)

        max_ball_for_pay = seller.get_max_ball_in_loyalty(actor, int(order.calculate_price_without_loyalty_balls()))
        if max_ball_for_pay > all_ball:
            max_ball_for_pay = all_ball

        special_products = seller.list_product()
        selected_products = order.list_easy_product()

        answer = {}
        answer['order_sum'] = int(order.calculate_price_without_loyalty_balls())
        answer['client'] = client
        answer['all_ball'] = all_ball
        answer['max_ball_for_pay'] = max_ball_for_pay
        answer['max_percent_in_loyalty'] = seller.get_max_percent_in_loyalty()
        answer['order_sum_with_ball'] = int(order.calculate_price_without_loyalty_balls()) - max_ball_for_pay
        answer['special_products'] = special_products
        answer['selected_products'] = selected_products
        template = loader.get_template('dcashier/static/newDealPage.html')
        context = RequestContext(request, answer)
        return HttpResponse(template.render(context.flatten()))

    def post(self, request, *args, **kwargs):
        actor = get_actor_for_request_if_login(request)
        seller = actor.get_seller()
        executor = seller.get_executor()
        order = seller.get_order_spec_id(request.session.get('order_id'))
        client = seller.get_customer_spec_id(request.session.get('client_id'))
        shop = get_shop_for_request_if_login(request)

        if not request.POST.get('action'):
            return redirect('/')

        if request.POST['action']  == 'set_product':
            order.delete_easy_products()
            for product_id in request.POST.getlist('products'):
                product = seller.get_product_spec_id(product_id)
                order.add(product, 1, 0, 'RUS')
            return redirect('/newDealPage.html')
        else:
            if request.POST['action']  == 'write_off':
                if seller.get_executor().is_size_xs():
                    seller.process_order_with_ball_type(order, 'MAX')
                elif seller.get_executor().is_size_s():
                    pickup_point = seller.get_pickup_point_spec_id(int(request.session.get('shop_id')))
                    seller.process_order_with_ball_type(order, 'MAX', pickup_point)
                else:
                    assert False
                template = loader.get_template('dcashier/static/transCompletedBallSpendPage.html')
                answer = {}
                reward_ball = seller.get_rewards_balls_for_order(order)
                answer['reward_ball_last_order'] = int(order.rewards_ball)
                context = RequestContext(request, answer)
                return HttpResponse(template.render(context.flatten()))

            elif request.POST['action']  == 'save_up':
                if seller.get_executor().is_size_xs():
                    seller.process_order_with_ball_type(order, 'ZERO')
                elif seller.get_executor().is_size_s():
                    pickup_point = seller.get_pickup_point_spec_id(int(request.session.get('shop_id')))
                    seller.process_order_with_ball_type(order, 'ZERO', pickup_point)
                else:
                    assert False
                template = loader.get_template('dcashier/static/transCompletedBallSavePage.html')
                answer = {}
                reward_ball = seller.get_rewards_balls_for_order(order)
                all_ball = seller.get_balance_customer_in_loyalty(client)
                answer['reward_ball_last_order'] = int(order.rewards_ball)
                answer['all_ball'] = int(all_ball)
                context = RequestContext(request, answer)
                return HttpResponse(template.render(context.flatten()))

            else:
                assert False

            reward_ball = seller.get_rewards_balls_for_order(order)
            request.session['price_last_order'] = int(order.calculate_price())
            request.session['reward_ball_last_order'] = int(reward_ball)
            return redirect('/')


class CustomerAddPage(View):
    def get(self, request, *args, **kwargs):
        actor = get_actor_for_request_if_login(request)
        if not request.session.get('actor_id'):
            return redirect('/')
        template = loader.get_template('dcashier/static/customerAddPage.html')
        answer = {}
        context = RequestContext(request, answer)
        return HttpResponse(template.render(context.flatten()))

    def post(self, request, *args, **kwargs):
        actor = get_actor_for_request_if_login(request)
        if not request.session.get('actor_id'):
            return redirect('/')

        seller = actor.get_seller()
        phone_number = request.POST['customerPhoneInput']
        title = request.POST['customerNameInput']
        sex = request.POST['selector']
        birthday = request.POST['customerBirthInput']
        phone_number_referee = request.POST['customerRefPhoneInput']

        if phone_number and \
            seller.has_customer_spec_phone_number(phone_number):
            client = seller.get_customer_spec_phone_number(phone_number)
            request.session['client_id'] = client.id

            template = loader.get_template('dcashier/static/customerAddPage.html')
            answer = {'error': 'Клиент с таким номером уже существует'}
            context = RequestContext(request, answer)
            return HttpResponse(template.render(context.flatten()))

        answer = {}
        if not phone_number or \
            not title or \
            not sex or \
            not birthday:
            template = loader.get_template('dcashier/static/customerAddPage.html')
            answer = {'error': 'Не коеректно заполнены поля'}
            context = RequestContext(request, answer)
            return HttpResponse(template.render(context.flatten()))

        if seller.has_customer_spec_phone_number(phone_number):
            client = seller.get_customer_spec_phone_number(phone_number)
            request.session['client_id'] = client.id

            template = loader.get_template('dcashier/static/customerAddPage.html')
            answer = {'error': 'Клиент с таким номером уже существует'}
            context = RequestContext(request, answer)
            return HttpResponse(template.render(context.flatten()))

        if request.POST['registration'] == 'zero':
            if seller.get_executor().is_size_xs() or \
                seller.get_executor().is_size_s():
                seller.create_customer(phone_number, title, sex, birthday, phone_number_referee)
            else:
                assert False
        elif request.POST['registration'] == '100':
            if seller.get_executor().is_size_xs() or \
                seller.get_executor().is_size_s():
                seller.create_customer_100(phone_number, title, sex, birthday, phone_number_referee)
                answer['registration_ball'] = 100
            else:
                assert False
        else:
            assert False

        client = seller.get_customer_spec_phone_number(phone_number)
        request.session['client_id'] = client.id

        template = loader.get_template('dcashier/static/customerAddedPage.html')
        answer['client'] = client
        context = RequestContext(request, answer)
        return HttpResponse(template.render(context.flatten()))

class CustomerAddedPage(View):
    def get(self, request, *args, **kwargs):
        actor = get_actor_for_request_if_login(request)
        if not request.session.get('actor_id'):
            return redirect('/')
        template = loader.get_template('dcashier/static/customerAddedPage.html')
        answer = {}
        context = RequestContext(request, answer)
        return HttpResponse(template.render(context.flatten()))

class TransConfirmSmsPage(View):
    def get(self, request, *args, **kwargs):
        actor = get_actor_for_request_if_login(request)
        if not request.session.get('actor_id'):
            return redirect('/')
        template = loader.get_template('dcashier/static/transConfirmSmsPage.html')
        answer = {}
        context = RequestContext(request, answer)
        return HttpResponse(template.render(context.flatten()))

class TransHistoryPage(View):
    def get(self, request, *args, **kwargs):
        if not request.session.get('actor_id'):
            return redirect('/')
        actor = get_actor_for_request_if_login(request)
        seller = actor.get_seller()
        if not request.session.get('shop_id'):
            return redirect('/')
        shop = get_shop_for_request_if_login(request)
        if shop.is_null():
            return redirect('/')

        customer = seller.get_customer_spec_id(request.session.get('client_id'))
        answer = {}
        answer['orders'] = seller.list_order_spec_customer(customer)
        answer['seller'] = seller.get_object()
        answer['client'] = customer

        template = loader.get_template('dcashier/static/transHistoryPage.html')
        context = RequestContext(request, answer)
        return HttpResponse(template.render(context.flatten()))

class TransCompletedBallSavePage(View):
    def get(self, request, *args, **kwargs):
        actor = get_actor_for_request_if_login(request)
        if not request.session.get('actor_id'):
            return redirect('/')
        template = loader.get_template('dcashier/static/transCompletedBallSavePage.html')
        answer = {}
        context = RequestContext(request, answer)
        return HttpResponse(template.render(context.flatten()))

class TransCompletedBallSpendPage(View):
    def get(self, request, *args, **kwargs):
        actor = get_actor_for_request_if_login(request)
        if not request.session.get('actor_id'):
            return redirect('/')
        template = loader.get_template('dcashier/static/transCompletedBallSpendPage.html')
        answer = {}
        context = RequestContext(request, answer)
        return HttpResponse(template.render(context.flatten()))


