# Generated by Django 5.0.3 on 2024-10-16 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0003_materiales_unidad_manejo'),
    ]

    operations = [
        migrations.AddField(
            model_name='materiales',
            name='cierre_gestion',
            field=models.IntegerField(default=False),
        ),
    ]
