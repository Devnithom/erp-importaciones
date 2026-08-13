from django.db import models
from catalogo.models import Producto
from django.core.exceptions import ValidationError

class Ubicacion(models.Model):
    TIPO_CHOICES = (
        ('ALMACEN', 'Almacén'),
        ('TIENDA', 'Tienda Física'),
    )
    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='ALMACEN')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

class Stock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)

    class Meta:
        # Una regla estricta de base de datos: 
        # Un mismo producto no puede tener dos filas en la misma ubicación.
        unique_together = ('producto', 'ubicacion')

    def __str__(self):
        return f"{self.producto.nombre} en {self.ubicacion.nombre}: {self.cantidad} und."

class Movimiento(models.Model): 
    TIPO_CHOICES = (
        ('ENTRADA', 'Entrada (Compra / Devolución)'),
        ('SALIDA', 'Salida (Venta / Merma / Traslado)'),
    )
    
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    motivo = models.CharField(max_length=200) 
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} | {self.producto.nombre} ({self.cantidad} und) | {self.motivo}"

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None # Verifica si es un movimiento nuevo, no una edición
        
        super().save(*args, **kwargs) # 1. Primero guarda el movimiento normal

        if es_nuevo:
            # 2. Busca el stock en esa ubicación. Si no existe, lo crea desde cero (0)
            stock_actual, creado = Stock.objects.get_or_create(
                producto=self.producto,
                ubicacion=self.ubicacion,
                defaults={'cantidad': 0}
            )

            # 3. Suma o resta la cantidad
            if self.tipo == 'ENTRADA':
                stock_actual.cantidad += self.cantidad
            elif self.tipo == 'SALIDA':
                if stock_actual.cantidad < self.cantidad:
                    raise ValidationError(f"Stock insuficiente. Intentas sacar {self.cantidad} und. pero solo hay {stock_actual.cantidad} disponibles.")
                stock_actual.cantidad -= self.cantidad

            # 4. Guarda el nuevo total en la tabla Stock
            stock_actual.save()