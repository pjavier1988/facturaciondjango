# Generated by Django 3.1.5 on 2021-07-03 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0013_facturaenc_estado_pago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturaenc',
            name='no_factura',
            field=models.IntegerField(auto_created=True),
        ),
    ]
