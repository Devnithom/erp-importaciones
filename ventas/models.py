from django.db import models
from catalogo.models import Producto
from inventario.models import Ubicacion, Movimiento

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    documento = models.CharField(max_length=20, unique=True, help_text="DNI o RUC")
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.documento})"

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT, help_text="Desde dónde se despacha")
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.nombre}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    # --- AUTOMATIZACIÓN DE VENTA A INVENTARIO ---
    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None
        super().save(*args, **kwargs) # Guardamos el detalle primero
        
        if es_nuevo:
            # 1. Sumamos el dinero al total de la venta
            self.venta.total += (self.cantidad * self.precio_unitario)
            self.venta.save()
            
            # 2. Ordenamos al almacén que retire el stock automáticamente
            Movimiento.objects.create(
                producto=self.producto,
                ubicacion=self.venta.ubicacion,
                tipo='SALIDA',
                cantidad=self.cantidad,
                motivo=f"Venta automatica #{self.venta.id}"
            )

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"