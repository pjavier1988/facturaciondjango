# Generated by Django 3.1.5 on 2021-08-28 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('param', '0011_merge_20210813_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='pais',
            field=models.CharField(choices=[('Ecuatoriano', 'Facebook'), ('Colombiano', 'Carousel')], default='Colombiano', max_length=20),
        ),
        migrations.AlterField(
            model_name='links',
            name='plataforma',
            field=models.CharField(choices=[('Facebook', 'Facebook'), ('Carousel', 'Carousel'), ('YouTube', 'YouTube'), ('Twitter', 'Twitter'), ('Instagram', 'Instagram'), ('LinkedIn', 'LinkedIn')], default='Carousel', max_length=20),
        ),
    ]
