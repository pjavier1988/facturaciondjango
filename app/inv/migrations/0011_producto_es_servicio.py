# Generated by Django 3.1.5 on 2021-02-05 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0010_producto_tiene_iva'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='es_servicio',
            field=models.BooleanField(default=False),
        ),
    ]
