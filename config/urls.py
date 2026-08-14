from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Importaciones ordenadas por aplicación
from django.contrib.auth import views as auth_views
from inventario.views import dashboard_view, ingreso_mercaderia_view, historial_movimientos_view, realizar_movimiento_view
from catalogo.views import inventario_visual_view
from ventas.views import nueva_venta_view
from inventario.views import dashboard_view, ingreso_mercaderia_view, historial_movimientos_view, realizar_movimiento_view, exportar_kardex_excel

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', dashboard_view, name='dashboard'),
    path('catalogo/', inventario_visual_view, name='inventario_visual'),
    path('ingreso/', ingreso_mercaderia_view, name='ingreso_mercaderia'),
    path('venta/', nueva_venta_view, name='nueva_venta'),
    path('historial/', historial_movimientos_view, name='historial'),
    path('movimientos/', realizar_movimiento_view, name='movimientos'),
    path('exportar-kardex/', exportar_kardex_excel, name='exportar_kardex'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)