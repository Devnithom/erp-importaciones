from django import forms
from .models import Movimiento

class IngresoMercaderiaForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['producto', 'ubicacion', 'cantidad', 'motivo']
        
        widgets = {
            'producto': forms.Select(attrs={'class': 'w-full bg-gray-800 text-white border border-gray-700 rounded p-2 mt-1'}),
            'ubicacion': forms.Select(attrs={'class': 'w-full bg-gray-800 text-white border border-gray-700 rounded p-2 mt-1'}),
            'cantidad': forms.NumberInput(attrs={'class': 'w-full bg-gray-800 text-white border border-gray-700 rounded p-2 mt-1', 'min': '1'}),
            'motivo': forms.TextInput(attrs={'class': 'w-full bg-gray-800 text-white border border-gray-700 rounded p-2 mt-1', 'placeholder': 'Ej. Importación, confección de taller...'}),
        }