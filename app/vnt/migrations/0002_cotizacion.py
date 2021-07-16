# Generated by Django 3.1.5 on 2021-07-06 18:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fac', '0016_auto_20210705_1042'),
        ('vnt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fc', models.DateTimeField(auto_now_add=True)),
                ('fm', models.DateTimeField(auto_now=True)),
                ('um', models.IntegerField(blank=True, null=True)),
                ('estado_cotizacion', models.TextField(choices=[('Enviado', 'Enviado'), ('Pendiente', 'Pendiente')], default='Enviado')),
                ('iva', models.FloatField(default=0)),
                ('descuento', models.FloatField(default=0)),
                ('envio', models.FloatField(default=0)),
                ('total', models.FloatField(default=0)),
                ('nota', models.TextField(max_length=300, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fac.cliente')),
                ('uc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
