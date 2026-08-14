from django.shortcuts import render, redirect
from catalogo.models import Producto
from inventario.models import Stock
from ventas.models import Venta
from django.db.models import Sum
from .forms import IngresoMercaderiaForm, TrasladoForm
from django.contrib import messages
from .models import Movimiento
from django.contrib.auth.decorators import login_required

@login_required
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

# --- NUEVA VISTA PARA EL FORMULARIO DE INGRESO ---
@login_required
def ingreso_mercaderia_view(request):
    if request.method == 'POST':
        form = IngresoMercaderiaForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.tipo = 'ENTRADA' # Candado: Forzamos que sea un ingreso
            movimiento.save() # Aquí se dispara la matemática automática hacia la tabla Stock
            return redirect('inventario_visual') # Lo mandamos al catálogo para que vea su stock sumado
    else:
        form = IngresoMercaderiaForm()
    
    return render(request, 'ingreso_mercaderia.html', {'form': form})

@login_required
def historial_movimientos_view(request):
    # Traemos todo el historial, del más nuevo al más viejo
    movimientos = Movimiento.objects.all().order_by('-fecha')
    return render(request, 'historial.html', {'movimientos': movimientos})

@login_required
def realizar_movimiento_view(request):
    if request.method == 'POST':
        form = TrasladoForm(request.POST)
        if form.is_valid():
            try:
                movimiento = form.save(commit=False)
                movimiento.tipo = 'TRASLADO' # Forzamos que sea traslado
                
                # Registramos qué usuario está haciendo la operación
                if request.user.is_authenticated:
                    movimiento.usuario = request.user
                    
                movimiento.save()
                return redirect('historial') # Lo enviamos a ver el kardex si tuvo éxito
                
            except Exception as e:
                # Si falla (ej. por falta de stock), sale alerta roja
                messages.error(request, str(e))
    else:
        form = TrasladoForm()
    
    return render(request, 'movimientos.html', {'form': form})