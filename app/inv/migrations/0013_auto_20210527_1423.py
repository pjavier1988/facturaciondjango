# Generated by Django 3.1.5 on 2021-05-27 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('param', '0004_auto_20210522_1435'),
        ('inv', '0012_producto_min_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='empresa',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='param.empresa'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='marca',
            name='empresa',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='param.empresa'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='empresa',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='param.empresa'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subcategoria',
            name='empresa',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='param.empresa'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unidadmedida',
            name='empresa',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='param.empresa'),
            preserve_default=False,
        ),
    ]
