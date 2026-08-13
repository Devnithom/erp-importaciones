from django.shortcuts import render
from catalogo.models import Producto
from inventario.models import Stock
from ventas.models import Venta
from django.db.models import Sum

def dashboard_view(request):
    # 1. Contar cuántos productos distintos existen
    total_productos = Producto.objects.count()
    
    # 2. Sumar todas las cantidades de la tabla Stock
    stock_agregado = Stock.objects.aggregate(total=Sum('cantidad'))
    total_stock = stock_agregado['total'] or 0
    
    # 3. Sumar todo el dinero de las Ventas registradas
    ventas_agregadas = Venta.objects.aggregate(total=Sum('total'))
    total_ventas = ventas_agregadas['total'] or 0

    # 4. Empaquetar los datos para enviarlos al HTML
    context = {
        'total_productos': total_productos,
        'total_stock': total_stock,
        'total_ventas': total_ventas,
    }
    return render(request, 'dashboard.html', context)