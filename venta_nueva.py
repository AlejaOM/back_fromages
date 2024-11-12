from rest_framework.test import APIClient
from django.urls import reverse

# Configura el cliente de API
client = APIClient()

# Obtén el token de autenticación
login_url = reverse("login")
login_data = {"nombre_usuario": "juanP", "password": "Juan123"}
login_response = client.post(login_url, login_data, format='json')

if login_response.status_code == 200:
    token = login_response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
else:
    print("Error en la autenticación:", login_response.json())
    exit()

# Define IDs de cliente, vendedor y productos existentes
cliente_id = 1
vendedor_id = 2
producto1_id = 1
producto2_id = 2

# Define los datos de la venta
data = {
    "cliente_id": cliente_id,
    "vendedor_id": vendedor_id,
    "productos": [
        {"producto_id": producto1_id, "cantidad": 2},
        {"producto_id": producto2_id, "cantidad": 1}
    ]
}

# URL para crear la venta
url = reverse("crear-venta")

# Realiza la solicitud POST para crear la venta
response = client.post(url, data, format='json')

# Verifica la respuesta
print("Status Code:", response.status_code)

# Muestra la respuesta JSON de la factura, asegurándote de que se incluya el número de factura y el total
response_json = response.json()
print("Response JSON:", response_json)

# Verifica si el número de factura y el total formateado están en la respuesta
if response.status_code == 201:
    numero_factura = response_json.get("numero_factura")
    total_formateado = response_json.get("total_formateado")
    detalles = response_json.get("detalles", [])
    
    print("Número de Factura:", numero_factura)
    print("Total Formateado:", total_formateado)
    print("Detalles de la Factura:")
    for detalle in detalles:
        print(f" - Producto: {detalle['producto']}, Cantidad: {detalle['cantidad']}, Precio Unitario: {detalle['precio_unitario_formateado']}, Precio Total: {detalle['precio_total_formateado']}")
else:
    print("Error al crear la venta:", response_json)
