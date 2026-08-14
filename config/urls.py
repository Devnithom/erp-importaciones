from django.contrib import admin
from django.urls import path
from inventario.views import dashboard_view, ingreso_mercaderia_view
from catalogo.views import inventario_visual_view
from django.conf import settings
from django.conf.urls.static import static
from ventas.views import nueva_venta_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventario/', inventario_visual_view, name='inventario_visual'),
    # Conectamos la ruta vacía '' con nuestra nueva función
    path('catalogo/', inventario_visual_view, name='inventario_visual'),
    path('ingreso/', ingreso_mercaderia_view, name='ingreso_mercaderia'),
    path('venta/', nueva_venta_view, name='nueva_venta'),
    path('', dashboard_view, name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
