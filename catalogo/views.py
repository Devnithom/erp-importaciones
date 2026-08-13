from django.shortcuts import render
from .models import Producto

def inventario_visual_view(request):
    # Traemos todos los productos que estén activos en la base de datos
    productos = Producto.objects.filter(activo=True)
    
    return render(request, 'inventario_visual.html', {'productos': productos})