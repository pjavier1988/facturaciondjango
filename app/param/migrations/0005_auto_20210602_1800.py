# Generated by Django 3.1.5 on 2021-06-02 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('param', '0004_auto_20210522_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='logo',
            field=models.FileField(null=True, upload_to='img/'),
        ),
    ]