# Generated by Django 3.1.5 on 2021-07-01 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0012_auto_20210605_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturaenc',
            name='estado_pago',
            field=models.TextField(choices=[('Pagado', 'Pagado'), ('Parcial', 'Parcial'), ('No Pagado', 'No Pagado')], default='Pagado'),
        ),
    ]
