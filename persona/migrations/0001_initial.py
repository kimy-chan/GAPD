# Generated by Django 5.0.3 on 2024-10-12 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula_identidad', models.CharField(error_messages={'unique': 'Ya existe la cedula de identidad registrada'}, max_length=20, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=60)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
