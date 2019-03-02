"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

#from dcashier.views import MyView, AuthPage, Login, Logout, index
from dcashier.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    #url(r'^$', MyView.as_view(), name='my-view'),
    #url(r'^index.html$', MyView.as_view(), name='my-view'),
    url(r'^$', Index.as_view(), name='my-view'),
    url(r'^index.html$', Index.as_view(), name='my-view'),
    url(r'^authPage.html$', AuthPage.as_view(), name='my-view'),
    url(r'^selectShopPage.html$', SelectShopPage.as_view(), name='my-view'),
    url(r'^shopPage.html$', ShopPage.as_view(), name='my-view'),
    url(r'^newDealPage.html$', NewDealPage.as_view(), name='my-view'),
    url(r'^sellerDealPage.html$', SellerDealPage.as_view(), name='my-view'),
    url(r'^customerAddPage.html$', CustomerAddPage.as_view(), name='my-view'),
    url(r'^customerAddedPage.html$', CustomerAddedPage.as_view(), name='my-view'),
    url(r'^transConfirmSmsPage.html$', TransConfirmSmsPage.as_view(), name='my-view'),
    url(r'^transHistoryPage.html$', TransHistoryPage.as_view(), name='my-view'),
    url(r'^transCompletedBallSavePage.html$', TransCompletedBallSavePage.as_view(), name='my-view'),
    url(r'^transCompletedBallSpendPage.html$', TransCompletedBallSpendPage.as_view(), name='my-view'),


    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='my-view'),
]
