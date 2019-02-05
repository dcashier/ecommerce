from django.contrib import admin
from eseller.models import Seller

class SellerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Seller, SellerAdmin)
