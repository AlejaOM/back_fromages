# populate_users.py
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fromages_back.settings')  # Cambia 'fromages' por el nombre de tu proyecto
django.setup()

from usuario.models import Usuario

usuarios = [
    {'documento': '1890786576', 'nombre': 'Juan', 'apellido': 'Perez', 'nombre_usuario': 'juanP', 'password': 'Juan123', 'rol': 'vendedor'},
    {'documento': '1298765477', 'nombre': 'Maria', 'apellido': 'Lopez', 'nombre_usuario': 'mariaL', 'password': 'Maria123', 'rol': 'vendedor'},
    {'documento': '1009876567', 'nombre': 'Pedro', 'apellido': 'Martinez', 'nombre_usuario': 'pedroM', 'password': 'Pedro123', 'rol': 'vendedor'},
    {'documento': '987465267', 'nombre': 'Mario', 'apellido': 'Torres', 'nombre_usuario': 'marioT', 'password': 'Mario123', 'rol': 'vendedor'},
    {'documento': '356678333', 'nombre': 'Veronica', 'apellido': 'Mendoza', 'nombre_usuario': 'veronicaM', 'password': 'Veronica123', 'rol': 'vendedor'},
    {'documento': '453824568', 'nombre': 'Pablo', 'apellido': 'Martinez', 'nombre_usuario': 'pabloM', 'password': 'Pablo123', 'rol': 'vendedor'},
    {'documento': '546457483', 'nombre': 'Diego', 'apellido': 'Paez', 'nombre_usuario': 'diegoP', 'password': 'Diego123', 'rol': 'vendedor'},
    {'documento': '377935645', 'nombre': 'Juan', 'apellido': 'Ramirez', 'nombre_usuario': 'juanR', 'password': 'JuanR123', 'rol': 'vendedor'},
    {'documento': '573673884', 'nombre': 'Maria', 'apellido': 'Ortega', 'nombre_usuario': 'mariaO', 'password': 'MariaO123', 'rol': 'vendedor'},
    {'documento': '324567891', 'nombre': 'Urbano', 'apellido': 'Gomez', 'nombre_usuario': 'urbanoG', 'password': 'UrbanoAdmin', 'rol': 'gerente'},
]

for user_data in usuarios:
    usuario = Usuario(
        documento=user_data['documento'],
        nombre=user_data['nombre'],
        apellido=user_data['apellido'],
        nombre_usuario=user_data['nombre_usuario'],
        rol=user_data['rol']
    )
    usuario.set_password(user_data['password'])  # Encripta la contraseña
    usuario.save()
