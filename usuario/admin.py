from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'documento', 'rol', 'nombre_usuario', 'is_active', 'is_staff')
    ordering = ['nombre_usuario']  # Cambia 'username' a 'nombre_usuario' o elimina esta línea si no necesitas ordenación.
