# Generated by Django 3.1.5 on 2021-02-04 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0006_auto_20210203_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturaenc',
            name='tipo',
            field=models.CharField(default='factura', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='facturaenc',
            name='no_factura',
            field=models.CharField(max_length=100),
        ),
    ]
