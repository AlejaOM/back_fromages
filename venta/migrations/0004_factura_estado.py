# Generated by Django 4.1 on 2024-11-16 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0003_alter_factura_numero_factura'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='estado',
            field=models.CharField(choices=[('borrador', 'Borrador'), ('cerrada', 'Cerrada')], default='borrador', max_length=10),
        ),
    ]
