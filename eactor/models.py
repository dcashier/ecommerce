#!-*-coding: utf-8 -*-
from django.db import models
from estorage.models import *
from django.contrib.auth.hashers import make_password

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

    def __has_link_with_actor(self, actor):
	print 'Nead fix __has_link_with_actor'
	return True

    def is_password(self, password):
        if self.password_hash == Actor.make_password_hash(password):
            return True
        return False

    @staticmethod
    def make_password_hash(password):
        return make_password(password, 'ttt', 'md5')

    def set_password(self, password):
        password_hash = Actor.make_password_hash(password)
        self.password_hash = password_hash
        self.save()

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
