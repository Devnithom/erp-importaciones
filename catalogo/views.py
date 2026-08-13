from django.shortcuts import render
from .models import Producto

def inventario_visual_view(request):
    # prefetch_related trae todos los stocks y ubicaciones en una sola consulta ultrarrápida
    productos = Producto.objects.filter(activo=True).prefetch_related('stock_set__ubicacion')
    
    return render(request, 'inventario_visual.html', {'productos': productos})