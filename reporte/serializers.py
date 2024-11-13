# reporte/serializers.py
from rest_framework import serializers
from venta import models
from venta.models import Factura, DetallesFactura
from django.db.models import Sum

class FacturaSerializer(serializers.ModelSerializer):
    numero_factura = serializers.CharField(source="numero_factura")
    cliente_nombre = serializers.CharField(source="cliente.nombre")
    cliente_apellido = serializers.CharField(source="cliente.apellido")
    fecha = serializers.DateTimeField(source="fecha")
    total = serializers.SerializerMethodField()

    class Meta:
        model = Factura
        fields = ["numero_factura", "cliente_nombre",  "cliente_apellido","fecha", "total"]

    def get_valorFactura(self, obj):
        total = obj.detalles.aggregate(total=Sum('total'))['total']
        return "${:,.2f}".format(total) if total else "$0.00"


class DetallesFacturaSerializer(serializers.ModelSerializer):
    producto_id = serializers.CharField(source="producto.id")
    producto_nombre = serializers.CharField(source="producto.nombre")
    precio_unitario = serializers.DecimalField(max_digits=10, decimal_places=2)
    precio_total = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = DetallesFactura
        fields = ["producto_id", "producto_nombre", "cantidad", "precio_unitario", "precio_total"]

class FacturaDetalleSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source="cliente.nombre")
    cliente_apellido = serializers.CharField(source="cliente.apellido")
    cliente_documento = serializers.CharField(source="cliente.documento")
    vendedor_nombre = serializers.CharField(source="vendedor.nombre")
    vendedor_apellido = serializers.CharField(source="vendedor.apellido")
    detalles = DetallesFacturaSerializer(many=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Factura
        fields = [
            "numero_factura", "fecha", "vendedor_nombre", "vendedor_apellido",
            "cliente_nombre", "cliente_apellido", "cliente_documento", "detalles", "total"
        ]

    def get_total(self, obj):
        return "${:,.2f}".format(obj.total)
 