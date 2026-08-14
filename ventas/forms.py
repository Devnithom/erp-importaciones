from django import forms
from .models import Cliente
from inventario.models import Ubicacion
from catalogo.models import Producto

class NuevaVentaForm(forms.Form):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        widget=forms.Select(attrs={'class': 'w-full bg-gray-800 text-white border border-gray-700 rounded p-2 mt-1'})
    )
    ubicacion = forms.ModelChoiceField(
        queryset=Ubicacion.objects.all(),
        label="Desde dónde sale (Almacén/Tienda)",
        widget=forms.Select(attrs={'class': 'w-full bg-gray-800 text-white border border-gray-700 rounded p-2 mt-1'})
    )
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(activo=True),
        widget=forms.Select(attrs={'class': 'w-full bg-gray-800 text-white border border-gray-700 rounded p-2 mt-1'})
    )
    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'w-full bg-gray-800 text-white border border-gray-700 rounded p-2 mt-1'})
    )
    precio_unitario = forms.DecimalField(
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'w-full bg-gray-800 text-white border border-gray-700 rounded p-2 mt-1', 'step': '0.10'})
    )