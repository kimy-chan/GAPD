# Generated by Django 5.0.3 on 2024-09-19 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proveedor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='prue',
            field=models.BooleanField(default=True),
        ),
    ]