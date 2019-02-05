from django.contrib import admin
from eloyalty.models import *

admin.site.register(LoyaltyRecord)
admin.site.register(LoyaltyPaymentPolicyRecord)
admin.site.register(LoyaltyPaymentPolicyPartRecord)
admin.site.register(LoyaltyAccountRecord)
admin.site.register(LoyaltyAccountBallInRecord)
admin.site.register(LoyaltyAccountBallOutRecord)
admin.site.register(LoyaltyTransactionRecord)

