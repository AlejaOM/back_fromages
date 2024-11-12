# reporte/urls.py
from django.urls import path
from .views import ReporteView , SucursalListView

urlpatterns = [
    path('facturas/', ReporteView.as_view(), name="reporte-facturas"),  
    path('sucursales/', SucursalListView.as_view(), name="sucursal-list")
]
