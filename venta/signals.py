from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Factura, DetallesFactura
from django.db.models import Max

@receiver(post_save, sender=Factura)
def asignar_numero_factura(sender, instance, created, **kwargs):
    if created and instance.numero_factura is None:
        ultimo_numero = Factura.objects.filter(numero_factura__isnull=False).aggregate(Max('numero_factura'))['numero_factura__max'] or 0
        instance.numero_factura = ultimo_numero + 1
        instance.save()

@receiver(post_save, sender=DetallesFactura)
@receiver(post_delete, sender=DetallesFactura)
def actualizar_total_factura(sender, instance, **kwargs):
    factura = instance.factura
    factura.total = sum(item.precio_total for item in factura.detalles.all())
    factura.save()