from django.db import models
from catalogo.models import Producto

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