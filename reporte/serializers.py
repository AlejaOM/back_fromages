# reporte/serializers.py
from rest_framework import serializers
from venta import models
from venta.models import Factura, DetallesFactura
from django.db.models import Sum

class FacturaSerializer(serializers.ModelSerializer):
    numeroFactura = serializers.CharField(source="numero_factura")
    clienteNombre = serializers.CharField(source="cliente.nombre")
    fechaFactura = serializers.DateTimeField(source="fecha")
    valorFactura = serializers.SerializerMethodField()

    class Meta:
        model = Factura
        fields = ["numeroFactura", "clienteNombre", "fechaFactura", "valorFactura"]

    def get_valorFactura(self, obj):
        total = obj.detalles.aggregate(total=Sum('precio_total'))['total']
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
    cliente_documento = serializers.CharField(source="cliente.documento")
    vendedor_nombre = serializers.CharField(source="vendedor.nombre")
    detalles = DetallesFacturaSerializer(many=True)

    class Meta:
        model = Factura
        fields = [
            "numero_factura", "fecha", "vendedor_nombre", "cliente_nombre", "cliente_documento", 
            "detalles", "total"
        ]
