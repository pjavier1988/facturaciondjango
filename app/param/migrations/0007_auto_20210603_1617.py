# Generated by Django 3.1.5 on 2021-06-03 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('param', '0006_auto_20210603_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='logo',
            field=models.FileField(null=True, upload_to='img/empresa'),
        ),
    ]
