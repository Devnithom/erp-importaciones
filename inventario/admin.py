from django.contrib import admin
from .models import Ubicacion, Stock, Movimiento

admin.site.register(Ubicacion)
admin.site.register(Stock)
admin.site.register(Movimiento)