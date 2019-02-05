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
    else:
        answer['is_login'] = False
        answer['test'] = 'TESTTT'
        answer['actor'] = 'actor'

    print '--'
    template = loader.get_template('dcashier/static/index.html')
    context = RequestContext(request, answer)
    #return HttpResponse(template.render(context))
    return HttpResponse(template.render(context.flatten()))

class ActorNone(object):
    def shops(self):
        return []

class AuthPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dcashier/static/authPage.html')

def __get_actor_for_request_if_login(request):
    if request.session.get('actor_id'):
        auth_system = AuthSystem()
        actor = auth_system.get_actor_by_id(request.session.get('actor_id'))
        return actor
    return ActorNone()

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
        actor = self.__get_actor_for_request_if_login(request)
        shops = actor.shops()

class ShopPage(View):
    def post(self, request, *args, **kwargs):
        actor = self.__get_actor_for_request_if_login(request)
        shops = actor.shops()
        seller = actor.seller()
        clent = get_client_by_phone(request.POST['phone_number'])
        order = seller.create_order([get_default_product], clent)


