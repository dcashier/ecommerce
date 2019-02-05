from django.contrib import admin
from eactor.models import Actor

class ActorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Actor, ActorAdmin)
