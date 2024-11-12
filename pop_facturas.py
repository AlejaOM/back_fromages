# populate_facturas.py
import django
import os

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fromages_back.settings')  # Cambia 'fromages_back' por el nombre de tu proyecto
django.setup()

from venta.models import Cliente, Producto, Factura, DetallesFactura
from django.contrib.auth import get_user_model

User = get_user_model()

# Datos para poblar facturas (relacionando clientes y vendedores existentes)
facturas_data = [
    {'cliente_id': 1, 'vendedor_id': 1},
    {'cliente_id': 2, 'vendedor_id': 2},
    {'cliente_id': 3, 'vendedor_id': 3},
    {'cliente_id': 4, 'vendedor_id': 4},
    {'cliente_id': 5, 'vendedor_id': 5},
    {'cliente_id': 6, 'vendedor_id': 6},
    {'cliente_id': 7, 'vendedor_id': 7},
    {'cliente_id': 8, 'vendedor_id': 8},
    {'cliente_id': 9, 'vendedor_id': 9},
]

for factura_data in facturas_data:
    cliente = Cliente.objects.get(id=factura_data['cliente_id'])
    vendedor = User.objects.get(id=factura_data['vendedor_id'])
    # Crear factura sin especificar manualmente el 'id' para evitar conflictos
    Factura.objects.create(cliente=cliente, vendedor=vendedor)

# Datos para poblar detalles de facturas
detalles_factura_data = [
    {'factura_id': 1, 'producto_id': 1, 'cantidad': 2, 'precio_unitario': 16000},
    {'factura_id': 1, 'producto_id': 2, 'cantidad': 1, 'precio_unitario': 9500},
    {'factura_id': 2, 'producto_id': 3, 'cantidad': 3, 'precio_unitario': 18000},
    {'factura_id': 2, 'producto_id': 4, 'cantidad': 2, 'precio_unitario': 15000},
    {'factura_id': 3, 'producto_id': 5, 'cantidad': 1, 'precio_unitario': 8000},
    {'factura_id': 3, 'producto_id': 6, 'cantidad': 2, 'precio_unitario': 22000},
    {'factura_id': 4, 'producto_id': 7, 'cantidad': 1, 'precio_unitario': 12000},
    {'factura_id': 4, 'producto_id': 8, 'cantidad': 1, 'precio_unitario': 15000},
    {'factura_id': 5, 'producto_id': 9, 'cantidad': 2, 'precio_unitario': 28000},
    {'factura_id': 5, 'producto_id': 10, 'cantidad': 1, 'precio_unitario': 17000},
    {'factura_id': 6, 'producto_id': 11, 'cantidad': 1, 'precio_unitario': 17500},
    {'factura_id': 6, 'producto_id': 12, 'cantidad': 2, 'precio_unitario': 26000},
    {'factura_id': 7, 'producto_id': 13, 'cantidad': 1, 'precio_unitario': 14000},
    {'factura_id': 7, 'producto_id': 14, 'cantidad': 1, 'precio_unitario': 16000},
    {'factura_id': 8, 'producto_id': 15, 'cantidad': 2, 'precio_unitario': 30000},
    {'factura_id': 8, 'producto_id': 16, 'cantidad': 1, 'precio_unitario': 15000},
    {'factura_id': 9, 'producto_id': 17, 'cantidad': 1, 'precio_unitario': 20000},
    {'factura_id': 9, 'producto_id': 18, 'cantidad': 1, 'precio_unitario': 18000},
    {'factura_id': 9, 'producto_id': 19, 'cantidad': 1, 'precio_unitario': 20000},
    {'factura_id': 9, 'producto_id': 20, 'cantidad': 2, 'precio_unitario': 35000},
]

for detalle_data in detalles_factura_data:
    factura = Factura.objects.get(numero_factura=detalle_data['factura_id'])
    producto = Producto.objects.get(id=detalle_data['producto_id'])
    DetallesFactura.objects.update_or_create(
        factura=factura,
        producto=producto,
        defaults={
            'cantidad': detalle_data['cantidad'],
            'precio_unitario': detalle_data['precio_unitario'],
            'precio_total': detalle_data['cantidad'] * detalle_data['precio_unitario']
        }
    )

print("Datos de facturas y detalles de facturas poblados correctamente.")
