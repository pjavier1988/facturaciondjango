# Generated by Django 3.1.5 on 2021-01-25 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0005_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='subcategoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inv.subcategoria'),
            preserve_default=False,
        ),
    ]
