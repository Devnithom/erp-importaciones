from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NuevaVentaForm
from .models import Venta, DetalleVenta
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test

def es_vendedor(user):
    # Da permiso si es Administrador (superuser) O si pertenece al grupo "Vendedores"
    return user.is_superuser or user.groups.filter(name='Vendedores').exists()

@login_required
def nueva_venta_view(request):
    # 1. SEGURIDAD DIRECTA AQUÍ DENTRO:
    es_admin = request.user.is_superuser
    es_vendedor = request.user.groups.filter(name='Vendedores').exists()
    
    # Si no es admin y tampoco es vendedor, lo pateamos con un mensaje de error
    if not (es_admin or es_vendedor):
        messages.error(request, "No tienes permiso para entrar a Ventas.")
        return redirect('inventario_visual')

    # 2. LÓGICA DE LA VENTA (Si pasó la seguridad)
    if request.method == 'POST':
        form = NuevaVentaForm(request.POST)
        if form.is_valid():
            try:
                venta = Venta.objects.create(
                    cliente=form.cleaned_data['cliente'],
                    ubicacion=form.cleaned_data['ubicacion'],
                    total=0
                )
                
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=form.cleaned_data['producto'],
                    cantidad=form.cleaned_data['cantidad'],
                    precio_unitario=form.cleaned_data['precio_unitario']
                )
                
                # OJO: Aquí la vendedora no puede ir al Dashboard, la regresamos al catálogo
                messages.success(request, "¡Venta registrada con éxito!")
                return redirect('inventario_visual')
                
            except ValidationError as e:
                venta.delete()
                messages.error(request, str(e.message))
    else:
        form = NuevaVentaForm()
        
    return render(request, 'nueva_venta.html', {'form': form})