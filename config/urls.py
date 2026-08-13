from django.contrib import admin
from django.urls import path
from inventario.views import dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # Conectamos la ruta vacía '' con nuestra nueva función
    path('', dashboard_view, name='dashboard'),
]