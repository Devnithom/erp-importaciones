from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    # Relación con Categoria
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    
    # Identificación
    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    
    # Precios
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Estado (Soft delete)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.sku}] {self.nombre}"