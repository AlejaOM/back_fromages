from django.urls import path
from .views import IniciarVentaView, ClienteView, ProductoView

urlpatterns = [
    path('clientes/', ClienteView.as_view(), name='clientes'),
    path('productos/', ProductoView.as_view(), name='productos'),
    path('iniciar-venta/', IniciarVentaView.as_view(), name='iniciar-venta'),
]
