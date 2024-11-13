from http import client
from rest_framework import serializers
from .models import Cliente, Producto, Factura, DetallesFactura
from django.db.models import Sum

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['documento', 'nombre', 'email', 'celular']

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'stock']

class DetallesFacturaSerializer(serializers.ModelSerializer):
    precio_unitario_formateado = serializers.SerializerMethodField()
    precio_total_formateado = serializers.SerializerMethodField()

    class Meta:
        model = DetallesFactura
        fields = ['producto', 'cantidad', 'precio_unitario_formateado', 'precio_total_formateado']

    def get_precio_unitario_formateado(self, obj):
        return "${:,.2f}".format(obj.precio_unitario)

    def get_precio_total_formateado(self, obj):
        return "${:,.2f}".format(obj.precio_total)

class FacturaSerializer(serializers.ModelSerializer):
    numero_factura = serializers.CharField()
    cliente_nombre = serializers.CharField(source="cliente.nombre")
    fecha = serializers.DateTimeField()
    total = serializers.SerializerMethodField()  # El campo se llama `total`

    class Meta:
        model = Factura
        fields = ["numero_factura", "cliente_nombre", "fecha", "total"]

    def get_total(self, obj):  # Cambia `get_valorFactura` por `get_total`
        total = obj.detalles.aggregate(total=Sum('precio_total'))['total']
        return "${:,.2f}".format(total) if total else "$0.00"

    
class CrearVentaSerializer(serializers.Serializer):
    cliente_id = serializers.IntegerField()
    productos = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        )
    )

    def validate(self, data):
        cliente_id = data.get('cliente_id')
        productos = data.get('productos')
      
        if not Cliente.objects.filter(id=cliente_id).exists():
            raise serializers.ValidationError("El cliente no existe.")
        
        for producto_data in productos:
            producto_id = producto_data.get('producto_id')
            cantidad = producto_data.get('cantidad')

            producto = Producto.objects.filter(id=producto_id).first()
            if not producto:
                raise serializers.ValidationError(f"Producto con id {producto_id} no encontrado.")
            if producto.stock < cantidad:
                raise serializers.ValidationError(f"Stock insuficiente para el producto {producto.nombre}.")
        
        return data

    def create(self, validated_data):
        cliente = Cliente.objects.get(id=validated_data['cliente_id'])
        vendedor = self.context['request'].user
        productos_data = validated_data['productos']

        # Creación de una factura temporal sin número asignado aún
        factura = Factura.objects.create(cliente=cliente, vendedor=vendedor)

        for producto_data in productos_data:
            producto = Producto.objects.get(id=producto_data['producto_id'])
            cantidad = producto_data['cantidad']

            # Descuenta el stock provisionalmente
            producto.stock -= cantidad
            producto.save()

            # Crea el detalle de la factura
            DetallesFactura.objects.create(  
                factura=factura,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio,  # Asignamos el precio actual del producto
                precio_total=producto.precio * cantidad
            )

        return factura
   