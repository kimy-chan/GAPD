# Generated by Django 5.0.3 on 2024-12-01 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proveedor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='ciudad',
            field=models.CharField(default='POTOSI', max_length=100),
        ),
    ]
