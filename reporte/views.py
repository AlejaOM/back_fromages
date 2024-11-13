from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from venta.models import Factura, DetallesFactura, Cliente
from .serializers import FacturaDetalleSerializer, FacturaSerializer, DetallesFacturaSerializer
from datetime import datetime

class ReporteView(APIView):
    def get(self, request):
        option = request.query_params.get("option")
        fecha_inicio = request.query_params.get("fecha_inicio")
        fecha_fin = request.query_params.get("fecha_fin")
        sucursal = request.query_params.get("sucursal", "Fromages")  # Valor por defecto "Fromages"

        
        if not fecha_inicio or not fecha_fin:
            return Response({"error": "Las fechas de inicio y fin son obligatorias"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Formato de fecha incorrecto, usa YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        if option == "facturas":
            facturas = Factura.objects.filter(fecha__date__range=[fecha_inicio, fecha_fin])

            if sucursal == "Fromages":
                facturas = facturas.filter(sucursal="Fromages")

            facturas = facturas.annotate(total_factura=Sum('detalles__precio_total'))
            serializer = FacturaSerializer(facturas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif option == "productos":
            detalles = DetallesFactura.objects.filter(factura__fecha__date__range=[fecha_inicio, fecha_fin])

            if sucursal == "Fromages":
                detalles = detalles.filter(factura__sucursal="Fromages")

            detalles = detalles.values('producto__id', 'producto__nombre').annotate(
                cantidadVendida=Sum('cantidad'),
                totalVentas=Sum('precio_total')
            )
            return Response(detalles, status=status.HTTP_200_OK)

        return Response({"error": "Opción no válida"}, status=status.HTTP_400_BAD_REQUEST)

class SucursalListView(APIView):
    def get(self, request):
        sucursales = [
            {"id": "1", "nombre": "Sucursal Fromages"}
        ]
        return Response(sucursales)
    
class FacturaDetalleView(APIView):
    def get(self, request, numero_factura):
        try:
            factura = Factura.objects.get(numero_factura=numero_factura)
            serializer = FacturaDetalleSerializer(factura)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Factura.DoesNotExist:
            return Response({"error": "Factura no encontrada."}, status=status.HTTP_404_NOT_FOUND)

class ReporteFacturasView(APIView):
    def get(self, request):
        fecha_inicio = request.query_params.get("fecha_inicio")
        fecha_fin = request.query_params.get("fecha_fin")

        if not fecha_inicio or not fecha_fin:
            return Response({"error": "Por favor proporciona ambas fechas (inicio y fin) en formato YYYY-MM-DD."},
                            status=status.HTTP_400_BAD_REQUEST)

        facturas = Factura.objects.filter(
            fecha__date__range=[fecha_inicio, fecha_fin]
        ).annotate(total_factura=Sum('detalles__precio_total'))

        serializer = FacturaSerializer(facturas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)