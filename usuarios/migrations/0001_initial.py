# Generated by Django 5.0.3 on 2024-10-12 01:54

import django.contrib.auth.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('persona', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Secretaria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secretaria', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Unidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('secretaria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='usuarios.secretaria')),
            ],
        ),
        migrations.CreateModel(
            name='Oficinas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('unidad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='usuarios.unidad')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=150, unique=True, verbose_name='Usuario')),
                ('password', models.CharField(max_length=128, verbose_name='Contraseña')),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('item', models.CharField(blank=True, max_length=100, null=True)),
                ('is_staff', models.CharField(default=True)),
                ('cargo', models.CharField(choices=[('Encargado_unidad', 'Inmedianto Superior'), ('Encargado_oficina', 'Responsable de la oficina'), ('Usuario', 'Personal de la oficina')], default='Usuario', verbose_name='Encargado de unidad')),
                ('crear', models.BooleanField(default=False, verbose_name='Crear material')),
                ('editar', models.BooleanField(default=False, verbose_name='editar material')),
                ('eliminar', models.BooleanField(default=False, verbose_name='Eliminar material')),
                ('rol', models.CharField(choices=[('Administrador', 'Administrador'), ('Super_administrador', 'Super administrador'), ('Auxiliar1', 'Auxiliar de Almacen'), ('Usuario', 'Usuario')], default='Personal', max_length=250)),
                ('es_habilitado', models.BooleanField(default=True)),
                ('es_activo', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='persona.persona')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('oficina', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='usuarios.oficinas')),
                ('unidad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='usuarios.unidad')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
