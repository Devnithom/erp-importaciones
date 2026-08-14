from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NuevaVentaForm
from .models import Venta, DetalleVenta
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

@login_required
def nueva_venta_view(request):
    if request.method == 'POST':
        form = NuevaVentaForm(request.POST)
        if form.is_valid():
            try:
                # 1. Crear la cabecera de la venta
                venta = Venta.objects.create(
                    cliente=form.cleaned_data['cliente'],
                    ubicacion=form.cleaned_data['ubicacion'],
                    total=0 # Se actualizará solo
                )
                
                # 2. Crear el detalle (Esto descuenta el stock automáticamente)
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=form.cleaned_data['producto'],
                    cantidad=form.cleaned_data['cantidad'],
                    precio_unitario=form.cleaned_data['precio_unitario']
                )
                
                return redirect('dashboard')
                
            except ValidationError as e:
                # Si no hay stock, capturamos el error rojo que hicimos ayer y lo mostramos bonito
                venta.delete() # Borramos la cabecera huérfana
                messages.error(request, str(e.message))
    else:
        form = NuevaVentaForm()
        
    return render(request, 'nueva_venta.html', {'form': form})