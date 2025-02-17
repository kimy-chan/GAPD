# Generated by Django 5.0.3 on 2024-12-23 02:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('persona', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresa', models.CharField(max_length=100)),
                ('nit', models.CharField(max_length=20)),
                ('telefono', models.CharField(max_length=20)),
                ('correo', models.EmailField(max_length=255)),
                ('descripcion', models.TextField(null=True)),
                ('pais', models.CharField(max_length=100)),
                ('ciudad', models.CharField(default='POTOSI', max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('es_habilitado', models.BooleanField(default=True)),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persona.persona')),
            ],
        ),
    ]
