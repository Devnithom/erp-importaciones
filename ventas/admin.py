from django.contrib import admin
from .models import Cliente, Venta, DetalleVenta

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1 # Muestra 1 fila vacía por defecto para agregar productos

class VentaAdmin(admin.ModelAdmin):
    inlines = [DetalleVentaInline]
    readonly_fields = ('total',) # El total se calcula solo, no se debe editar a mano

admin.site.register(Cliente)
admin.site.register(Venta, VentaAdmin)