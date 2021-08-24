# Generated by Django 3.1.5 on 2021-01-26 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0003_auto_20190831_2250'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='identificacion',
            field=models.CharField(max_length=13,blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='facturadet',
            name='detiva',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='facturaenc',
            name='faciva',
            field=models.FloatField(default=0),
        ),
    ]