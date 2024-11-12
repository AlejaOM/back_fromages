from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cliente, Producto, Factura, DetallesFactura
from .serializers import ClienteSerializer, ProductoSerializer, FacturaSerializer, CrearVentaSerializer
from rest_framework import status
from django.db import transaction
from rest_framework import serializers
from django.db.models import Max
from rest_framework.permissions import BasePermission

class ClienteView(APIView):
    def get(self, request, documento):
        cliente = Cliente.objects.filter(documento=documento).first()
        if cliente:
            serializer = ClienteSerializer(cliente)
            return Response(serializer.data)
        return Response({'error': 'Cliente no encontrado'}, status=404)

class ProductoView(APIView):
    def get(self, request):
        query = request.GET.get('query')
        productos = Producto.objects.filter(nombre__icontains=query) | Producto.objects.filter(id=query)
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)
    
class IsVendedorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.rol == "vendedor"

class IniciarVentaView(APIView):
    permission_classes = [IsVendedorPermission]
    def post(self, request):
        serializer = CrearVentaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            factura = serializer.save()
            factura_serializer = FacturaSerializer(factura)
            return Response(factura_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CerrarVentaView(APIView):
    def post(self, request, factura_id):
        try:
            factura = Factura.objects.get(id=factura_id, numero_factura__isnull=True)  # Factura temporal sin número asignado
            with transaction.atomic():
                ultimo_numero = Factura.objects.filter(numero_factura__isnull=False).aggregate(Max('numero_factura'))['numero_factura__max'] or 0
                factura.numero_factura = ultimo_numero + 1
                factura.save()

                # Confirma el stock y ajusta los productos
                for detalle in factura.detalles.all():
                    producto = detalle.producto
                    if producto.stock < detalle.cantidad:
                        raise serializers.ValidationError(f"Stock insuficiente para el producto {producto.nombre}.")
                    producto.stock -= detalle.cantidad
                    producto.save()

            return Response({'message': 'Venta realizada exitosamente', 'factura_id': factura.id, 'numero_factura': factura.numero_factura})
        except Factura.DoesNotExist:
            return Response({'error': 'Factura no encontrada o ya cerrada'}, status=status.HTTP_404_NOT_FOUND)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
