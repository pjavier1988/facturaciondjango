# Generated by Django 3.1.5 on 2021-08-11 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('param', '0008_links'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='tributa',
            field=models.BooleanField(default=True),
        ),
    ]
