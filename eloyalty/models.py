#!-*-coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from eshop.models import *
import datetime
from django.utils import timezone


class Loyalty(object):
    # Пока не понятно что делать с просроченными балами, как их списывать?
    # Если это не делать то вся сумма выдееленая клиенту магазину для расчета с клиентами осядет на клиентах как не используемая.
    def calculate_reward(self, actor, spent_money):
        payment_policies = LoyaltyPaymentPolicyRecord.objects.filter(loyalty=self.__record)
        payment_policy = payment_policies[0]
        return payment_policy.calculate_reward(spent_money)

    def __count_transaction(self, samebody):
        account_record = self.__get_account_for_samebody(samebody)
        count = 0
        count += LoyaltyAccountBallInRecord.objects.filter(loyalty=self.__record, account=account_record).count()
        count += LoyaltyAccountBallOutRecord.objects.filter(loyalty=self.__record, account=account_record).count()
        return count

    def __create_account_for_samebody(self, samebody):
        #entity_record = samebody.get_record()
        entity_record = samebody
        account_record = LoyaltyAccountRecord(owner=entity_record, loyalty=self.__record)
        account_record.save()

    def create_range_ball(self, actor, cost):
        return [0, int(cost * self.__record.max_percent / 100)]

    def __get_account_for_samebody(self, samebody):
        #entity_record = samebody.get_record()
        entity_record = samebody
        account_record = LoyaltyAccountRecord.objects.get(owner=entity_record, loyalty=self.__record)
        return account_record

    def get_balance(self, actor, samebody, datetime_for_check):
        if not self.__has_account_for_samebody(samebody):
            print u'Error : Пользователь не зарегестрирован в системе лояльности.'
            assert False
        account_record = self.__get_account_for_samebody(samebody)
        ball_sum = 0
        #datetime_for_check = datetime.datetime.now()
        datetime_for_check = timezone.now()
        datetime_for_check_str = datetime_for_check.strftime("%Y-%m-%d %H:%M:%S")
        datetime_for_check_str = datetime_for_check
        for ball in LoyaltyAccountBallInRecord.objects.filter(
            account=account_record,
            available_before_date__gt=datetime_for_check_str,
            loyalty=self.__record,
            ):
            ball_sum += ball.ball
        for ball in LoyaltyAccountBallOutRecord.objects.filter(account=account_record, loyalty=self.__record):
            ball_sum -= ball.ball
        return ball_sum

    def get_record(self):
        return self.__record

    def get_max_percent(self):
        # fot test
        return self.__record.max_percent

    def get_start_ball(self):
        # fot test
        return self.__record.start_ball

    def get_title(self):
        return self.__record.title

    def __has_account_for_samebody(self, samebody):
        #entity_record = samebody.get_record()
        entity_record = samebody
        if LoyaltyAccountRecord.objects.filter(owner=entity_record, loyalty=self.__record).count() > 0:
            return True
        return False

    def __in_ball(self, transaction_record, samebody, ball, available_day):
        day_delta = datetime.timedelta(days=available_day)
        #available_before_date = datetime.datetime.now() + day_delta
        available_before_date = timezone.now() + day_delta
        account_record = self.__get_account_for_samebody(samebody)
        ball_in_acount_record = LoyaltyAccountBallInRecord(
            account=account_record,
            ball=ball,
            available_day=available_day,
            available_before_date=available_before_date,
            loyalty=self.__record
            )
        ball_in_acount_record.save()
        transaction_record.ball_in = ball_in_acount_record
        transaction_record.save()

    def __init__(self, record):
        self.__record = record

    def is_allow_ball(self, actor, range_ball, ball_customer):
        if range_ball[0] <= ball_customer and ball_customer <= range_ball[1]:
            return True
        return False

    def __is_need_auth(self):
        return self.__record.is_need_auth

    def __is_registration(self, samebody):
        #if self.__has_account_for_samebody(samebody) and self.__count_transaction(samebody) > 0:
        if self.__has_account_for_samebody(samebody):
            return True
        return False

    def is_registration(self, actor, samebody):
        return self.__is_registration(samebody)

    def list_customer(self, actor, samebody):
        owners = []
        for lar in LoyaltyAccountRecord.objects.filter(loyalty=self.__record):
            owners.append(Customer(lar.owner))
        return owners

    def list_transaction(self, actor, samebody):
        if not samebody.is_allow_list_transaction_this(actor):
            print u'Error : Нет прав'
            assert False
        account_record = self.__get_account_for_samebody(samebody)
        balls = []
        for ball in LoyaltyAccountBallInRecord.objects.filter(loyalty=self.__record, account=account_record):
            balls.append({'ball': ball.ball})
        for ball in LoyaltyAccountBallOutRecord.objects.filter(loyalty=self.__record, account=account_record):
            balls.append({'ball': ball.ball})
        return balls

    def __out_ball(self, transaction_record, samebody, ball):
        account_record = self.__get_account_for_samebody(samebody)
        ball_out_acount_record = LoyaltyAccountBallOutRecord(account=account_record, ball=ball, loyalty=self.__record)
        ball_out_acount_record.save()
        transaction_record.ball_out = ball_out_acount_record
        transaction_record.save()

    def __register_in_loyalty_customer(self, actor, customer, executor, hello_ball, available_day):
        if not self.__is_registration(customer):
            self.__create_account_for_samebody(customer)
            if hello_ball > 0:
                self.transfer_ball(actor, executor, customer, hello_ball, available_day)
            else:
                print 'Error : customer registration without hello ball.'
        else:
            print 'Error : customer is not registration'
            assert False

    def register_in_loyalty_executor(self, executor, reward_percent, available_day, start_ball, start_ball_available_day):
        self.__create_account_for_samebody(executor)
        if reward_percent:
            payment_policy_record = LoyaltyPaymentPolicyRecord(loyalty=self.__record)
            payment_policy_record.save()
            payment_policy_record.add_part(reward_percent, available_day)
        transaction_record = LoyaltyTransactionRecord(title='Создание системы лояльности', loyalty=self.__record)
        transaction_record.save()
        self.__in_ball(transaction_record, executor, start_ball, start_ball_available_day)
        transaction_record.is_ok = True
        transaction_record.save()

    def register_in_loyalty_hello_0(self, actor, customer, executor):
        if self.is_registration(actor, customer):
            print 'Error : customer is already registration in loyalty'
            assert False
        hello_ball = 0
        available_day = 30
        self.__register_in_loyalty_customer(actor, customer, executor, hello_ball, available_day)

    def register_in_loyalty_hello_1000(self, actor, customer, executor):
        if self.is_registration(actor, customer):
            print 'Error : customer is already registration in loyalty'
            assert False
        hello_ball = 1000
        available_day = 30
        self.__register_in_loyalty_customer(actor, customer, executor, hello_ball, available_day)

    def __str__(self):
        return (u"Loyalty : %s" % (self.__record.title)).encode('utf-8')

    def transfer_ball(self, actor, samebody_from, samebody_to, ball, available_day):
        # открыли транзакцию
        datetime_for_check = datetime.datetime.now()
        if ball <= 0:
            print u'Error : Разрешен перевод только положительной суммы балов'
            assert False
        if self.get_balance(actor, samebody_from, datetime_for_check) < ball:
            print u'Error : Нельзя уходить в минуc'
            assert False
            return
        if not samebody_from.is_allow_send_ball_this(actor):
            if self.__is_need_auth():
                print u'Error : Нет прав у %s для изменний в %s' % (actor, samebody_from)
                assert False
            elif not self.__is_need_auth():
                text_p = u'Alert : Хотя нет прав у %s для изменний в %s, '% (actor, samebody_from)
                text_p += u'данная система лояльности позвоялет переводить балы между объектам без их согласия.'
                print text_p.encode('utf-8')
        if not self.__is_registration(samebody_to):
            print u'Error : Пользователь не зарегистрированн в системе лойльности'
            assert False
        transaction_record = LoyaltyTransactionRecord(title=u'Перевод балов кем %s откуда %s куда %s сколько %s' % (actor, samebody_from, samebody_to, ball), loyalty=self.__record)
        transaction_record.save()
        self.__out_ball(transaction_record, samebody_from, ball)
        #transaction_record.ball_in = None
        #transaction_record.save()
        self.__in_ball(transaction_record, samebody_to, ball, available_day)
        #transaction_record.ball_out = None
        #transaction_record.save()
        transaction_record.is_ok = True
        transaction_record.save()
        # закрыли транзакцию
        print 'Info : transfer_ball is OK'

    def __unicode__(self):
        return u"Loyalty : %s" % (self.__record.title)


class ServiceRepositoryLoyalty(object):
    @classmethod
    def create_loyalty(cls, actor, executor, title, max_percent, start_ball, start_ball_available_day, reward_percent, available_day, is_need_auth):
        #executor_record = executor.get_record()
        executor_record = executor
        loyalty_record = LoyaltyRecord(title=title, max_percent=max_percent, start_ball=start_ball, owner=executor_record, is_need_auth=is_need_auth)
        loyalty_record.save()
        loyalty = Loyalty(loyalty_record)
        loyalty.register_in_loyalty_executor(executor, reward_percent, available_day, start_ball, start_ball_available_day)

    @classmethod
    def has_loyalty_for_owner(cls, client, owner):
        if cls.list_loyalty_for_owner(client, owner):
            return True
        return False

    @classmethod
    def list_loyalty_for_owner(cls, client, owner):
        """
        Список систем лояльности в которых учатсвует данный магазин.
            а вообще данному клиенту позволено видеть все системы данного миагазина или только часть.
        """
        if not owner.is_allow_all_loyalty_for_client(client):
            raise u""
            print 'Error : list_loyalty_for_owner'
        loyalties = []
        #for loyalty_record in LoyaltyRecord.objects.filter(owner=owner.get_record()):
        for loyalty_record in LoyaltyRecord.objects.filter(owner=owner):
            loyalties.append(Loyalty(loyalty_record))
        return loyalties

    @classmethod
    def save_loyalty(cls, loyalty):
        pass


class LoyaltyRecord(models.Model):
    owner = models.ForeignKey(Shop, null=True, blank=True)
    title = models.CharField(verbose_name=u'Название', max_length=128, null=True, blank=True)
    max_percent = models.IntegerField(u'Максимальный процент от суммы заказа для оплаты балами')
    start_ball = models.IntegerField(u'Стартовые былы')
    is_need_auth = models.BooleanField(verbose_name=u'Требуется подтвержение переводов', default=True)


class LoyaltyPaymentPolicyRecord(models.Model):
    loyalty = models.ForeignKey(LoyaltyRecord)

    def add_part(self, reward_percent, available_day):
        payment_policy_part_record = LoyaltyPaymentPolicyPartRecord(payment_policy=self, percent=reward_percent, available_day=available_day)
        payment_policy_part_record.save()

    def calculate_reward(self, spent_money):
        reward_money = 0
        day = 0
        for payment_policy_part_record in LoyaltyPaymentPolicyPartRecord.objects.filter(payment_policy=self):
            if payment_policy_part_record.is_allow_money(spent_money):
                reward_money = spent_money * payment_policy_part_record.percent / 100
                day = payment_policy_part_record.available_day
                break
        else:
            print 'Error : Not set reward for money range'
            assert False
        return {'ball': reward_money, 'day': day}


class LoyaltyPaymentPolicyPartRecord(models.Model):
    #loyalty = models.ForeignKey(LoyaltyRecord)
    payment_policy = models.ForeignKey(LoyaltyPaymentPolicyRecord)
    percent = models.IntegerField(u'Процент начисления')
    min_money = models.IntegerField(u'Начало диапазона', null=True, blank=True)
    max_money = models.IntegerField(u'Конец диапазона(включая данное значение)', null=True, blank=True)
    available_day = models.IntegerField(u'Возможность потратить балы на протяжении стольких дней с момента их начисления')

    def is_allow_money(self, money):
        if (not self.min_money or self.min_money < money) and (money <= self.max_money or not self.max_money):
            return True
        return False


class LoyaltyAccountRecord(models.Model):
    loyalty = models.ForeignKey(LoyaltyRecord)
    owner = models.ForeignKey(Shop)


class LoyaltyAccountBallInRecord(models.Model): # приход
    loyalty = models.ForeignKey(LoyaltyRecord)
    account = models.ForeignKey(LoyaltyAccountRecord)
    ball = models.IntegerField(u'колличество')
    datetime_create = models.DateTimeField(u'Дата и время создания', auto_now_add=True)
    available_day = models.IntegerField(u'Возможность потратить балы на протяжении стольких дней с момента их начисления', null=True, blank=True)
    available_before_date = models.DateTimeField(u'Дата до которой можно потратить балы', null=True, blank=True)


class LoyaltyAccountBallOutRecord(models.Model): # расход
    loyalty = models.ForeignKey(LoyaltyRecord)
    account = models.ForeignKey(LoyaltyAccountRecord)
    ball = models.IntegerField(u'колличество')
    datetime_create = models.DateTimeField(u'Дата и время создания', auto_now_add=True)


class LoyaltyTransactionRecord(models.Model):
    loyalty = models.ForeignKey(LoyaltyRecord)
    ball_in = models.ForeignKey(LoyaltyAccountBallInRecord, null=True, blank=True)
    #account_in = models.ForeignKey(LoyaltyAccountRecord, related_name="%(app_label)s_%(class)s_in_relate")
    ball_out = models.ForeignKey(LoyaltyAccountBallOutRecord, null=True, blank=True)
    #account_out = models.ForeignKey(LoyaltyAccountRecord, related_name="%(app_label)s_%(class)s_out_relate")
    title = models.CharField(verbose_name=u'Название', max_length=255, null=True, blank=True)
    is_ok = models.BooleanField(u'Транзакция закончена успешно', default=False)


