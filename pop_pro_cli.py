# populate_data.py
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fromages_back.settings')  # Cambia 'fromages' por el nombre de tu proyecto
django.setup()

from venta.models import Cliente, Producto

clientes = [
    {'documento': '1890786576', 'nombre': 'Juan Alban', 'email': None, 'celular': None},
    {'documento': '1298765477', 'nombre': 'Maria Cordero', 'email': None, 'celular': None},
    {'documento': '1009876567', 'nombre': 'Pedro Pinto', 'email': None, 'celular': None},
    {'documento': '1876090006', 'nombre': 'Pablo Ponce', 'email': None, 'celular': None},
    {'documento': '1893456776', 'nombre': 'Lorena Paz', 'email': None, 'celular': None},
    {'documento': '1678999891', 'nombre': 'Rosario Utreras', 'email': None, 'celular': None},
    {'documento': '1244567888', 'nombre': 'Leticia Ortega', 'email': None, 'celular': None},
    {'documento': '1456799022', 'nombre': 'Juan Torres', 'email': None, 'celular': None},
    {'documento': '1845677777', 'nombre': 'Jorge Parra', 'email': None, 'celular': None},
    {'documento': '183445667', 'nombre': 'Pablo Polit', 'email': None, 'celular': None},
]

for cliente_data in clientes:
    Cliente.objects.create(**cliente_data)

# Datos de productos
productos = [
    {'nombre': 'Queso Doble Crema', 'precio': 8000, 'stock': 60},
    {'nombre': 'Queso Mozzarella', 'precio': 9500, 'stock': 32},
    {'nombre': 'Queso Campesino', 'precio': 6000, 'stock': 30},
    {'nombre': 'Queso Criollo', 'precio': 7500, 'stock': 17},
    {'nombre': 'Queso Costeño', 'precio': 8000, 'stock': 65},
    {'nombre': 'Queso Pera', 'precio': 11000, 'stock': 40},
    {'nombre': 'Queso Saravena', 'precio': 12000, 'stock': 30},
    {'nombre': 'Queso Gouda', 'precio': 15000, 'stock': 35},
    {'nombre': 'Queso Parmesano', 'precio': 14000, 'stock': 35},
    {'nombre': 'Queso Gruyere', 'precio': 17000, 'stock': 29},
    {'nombre': 'Queso Camembert', 'precio': 17500, 'stock': 24},
    {'nombre': 'Queso Provolone', 'precio': 13000, 'stock': 33},
    {'nombre': 'Queso Emmental', 'precio': 14000, 'stock': 24},
    {'nombre': 'Queso Brie', 'precio': 16000, 'stock': 29},
    {'nombre': 'Queso Cottage', 'precio': 15000, 'stock': 28},
    {'nombre': 'Queso Feta', 'precio': 15000, 'stock': 32},
    {'nombre': 'Queso Suizo', 'precio': 20000, 'stock': 15},
    {'nombre': 'Queso Izmir Tulum', 'precio': 18000, 'stock': 35},
    {'nombre': 'Queso Gorgonzola', 'precio': 20000, 'stock': 15},
    {'nombre': 'Queso Port Salut', 'precio': 17500, 'stock': 35},
]

# Insertar productos
for producto_data in productos:
    Producto.objects.create(**producto_data)
