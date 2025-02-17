# Generated by Django 5.0.3 on 2024-12-23 02:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('material_compras', '0001_initial'),
        ('proveedor', '0001_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='matarial_compras',
            name='oficina',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='usuarios.oficinas'),
        ),
        migrations.AddField(
            model_name='matarial_compras',
            name='proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='proveedor.proveedor'),
        ),
        migrations.AddField(
            model_name='matarial_compras',
            name='secretaria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='usuarios.secretaria'),
        ),
        migrations.AddField(
            model_name='matarial_compras',
            name='unidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='usuarios.unidad'),
        ),
        migrations.AddField(
            model_name='matarial_compras',
            name='numero_registro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='material_compras.numero_registro'),
        ),
    ]
