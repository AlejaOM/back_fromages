# Generated by Django 4.1 on 2024-11-16 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
    ]
