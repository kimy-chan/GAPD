# Generated by Django 5.0.3 on 2024-11-15 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0004_rename_aprobado_secretario_pedido_aprobado_cardista'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='aprobado_cardista_segunda',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='descripcion',
            field=models.TextField(null=True),
        ),
    ]