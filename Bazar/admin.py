from django.contrib import admin

from .models import Evento, Item, Usuario

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Item)
admin.site.register(Evento)
