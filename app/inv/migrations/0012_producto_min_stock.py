# Generated by Django 3.1.5 on 2021-05-25 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0011_producto_es_servicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='min_stock',
            field=models.IntegerField(default=0),
        ),
    ]