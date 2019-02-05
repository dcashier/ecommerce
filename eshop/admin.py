from django.contrib import admin
from eshop.models import Shop

class ShopAdmin(admin.ModelAdmin):
    pass
admin.site.register(Shop, ShopAdmin)
