#!-*-coding: utf-8 -*-
from django.db import models
from estorage.models import *
from django.contrib.auth.hashers import make_password
from eseller.models import *

class Actor(models.Model):
    """
    Аккаунты действущих лиц.
    Нужны для совершения действий на ппроекте.
    """
    title = models.CharField(verbose_name=u'Название Ип / ооо / оао', max_length=254, null=True, blank=True)
    is_person = models.BooleanField(verbose_name=u'Человек/Робот', default=False)
    birthday = models.DateField(u'Дата рождения', null=True, blank=True)
    phone_number = models.CharField(verbose_name=u'Номер мобильного', max_length=128, null=True, blank=True)
    phone_m_type = models.CharField(verbose_name=u'Тип номера мобильного', max_length=128, null=True, blank=True)
    fio = models.CharField(verbose_name=u'Ф.И.О.', max_length=128, null=True, blank=True)
    password_hash = models.CharField(verbose_name=u'Хеш пароля', max_length=128, null=True, blank=True)
    seller = models.ForeignKey(Seller, null=True, blank=True)
    purchaser = models.ForeignKey(Purchaser, null=True, blank=True)

    def create_customer_shop_with_phone_number(self, shop, phone_number):
        self.seller.create_customer_shop_with_phone_number(shop, phone_number)

    def get_customer_spec_executor_phone_number(self, shop, phone_number):
        return self.seller.get_customer_spec_executor_phone_number(shop, phone_number)
        #from eshop.models import *
        #return Shop(phone_number='+71002003040')

    def get_seller(self):
        if self.seller.get_shop_size() == 'xs':
            return SellerXS(self.seller)
        elif self.seller.get_shop_size() == 's':
            return SellerS(self.seller)
        assert False

    def has_customer_spec_executor(self, shop, client):
        if self.seller.has_customer_spec_executor(shop, client):
            return True
        return False

    def has_customer_spec_executor_phone_number(self, shop, phone_number):
        if self.seller.has_customer_spec_executor_phone_number(shop, phone_number):
            return True
        return False

    def __has_link_with_actor(self, actor):
	print 'Nead fix __has_link_with_actor'
	return True

    def is_password(self, password):
        if self.password_hash == Actor.make_password_hash(password):
            return True
        return False

    def is_seller_shop(self, shop):
        if self.seller and self.seller.is_work_in_shop(shop):
            return True
        return False

    @staticmethod
    def make_password_hash(password):
        #return make_password(password, 'ttt', 'md5') # не проходят тесты в docker
        return make_password(password, 'ttt')

    def set_password(self, password):
        password_hash = Actor.make_password_hash(password)
        self.password_hash = password_hash
        self.save()

    def shops(self):
        """
        Список магазинов которыми может управлять продавец ассоцированный с данной учетной записью
        """
        assert False
        if self.seller:
            #return self.seller.shops()
            return self.seller.list_shop()
        return []

    def __unicode__(self):
        return u"%s: [%s] %s - %s (%s)" % (self.id, 'Man' if self.is_person else 'Robot', self.title, self.phone_number, self.fio)


class AuthSystem(object):
    def has_actor_by_phone_numnber_password(self, phone_number, password):
        for actor in Actor.objects.filter(phone_number=phone_number, password_hash=Actor.make_password_hash(password)):
            return True
        return False

    def get_actor_by_phone_numnber_password(self, phone_number, password):
        return Actor.objects.filter(phone_number=phone_number, password_hash=Actor.make_password_hash(password))[0]

    def get_actor_by_id(self, actor_id):
        return Actor.objects.get(id=actor_id)
