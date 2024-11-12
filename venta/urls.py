from django.urls import path

from venta import views
from .views import IniciarVentaView, CerrarVentaView , ClienteView, ProductoView

urlpatterns = [
    path('clientes/', views.ClienteView.as_view(), name='clientes'),
    path('productos/', views.ProductoView.as_view(), name='productos'),
    path('crear-venta/', IniciarVentaView.as_view(), name='crear-venta'),
    path('cerrar-venta/<int:factura_id>/', CerrarVentaView.as_view(), name='cerrar-venta'),
]

