# Generated by Django 3.1.5 on 2021-08-13 05:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('param', '0009_auto_20210813_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='links',
            name='empresa',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='param.empresa'),
            preserve_default=False,
        ),
    ]
