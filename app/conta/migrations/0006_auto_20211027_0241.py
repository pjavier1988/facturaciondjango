# Generated by Django 3.1.5 on 2021-10-27 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conta', '0005_auto_20211027_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleadohoraextra',
            name='fecha',
            field=models.DateField(),
        ),
    ]
