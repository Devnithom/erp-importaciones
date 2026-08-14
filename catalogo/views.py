from django.shortcuts import render
from .models import Producto
from django.db.models import Q # Herramienta para buscar en varios campos a la vez
from django.contrib.auth.decorators import login_required

@login_required
def inventario_visual_view(request):
    # Obtenemos lo que el usuario escribió en el buscador (por defecto, nada)
    query = request.GET.get('q', '')
    
    # Base: Traemos todos los productos activos con sus stocks
    productos = Producto.objects.filter(activo=True).prefetch_related('stock_set__ubicacion')
    
    # Si el usuario buscó algo, filtramos los resultados
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | 
            Q(sku__icontains=query) |
            Q(categoria__nombre__icontains=query)
        )
    
    # Enviamos la lista (filtrada o no) y también la palabra buscada (para dejarla escrita en la barra)
    return render(request, 'inventario_visual.html', {'productos': productos, 'query': query})