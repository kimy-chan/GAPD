# Generated by Django 5.0.3 on 2024-12-01 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0003_pedido_aprobado_cardista_segunda_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='numero_pedido',
            field=models.CharField(blank=True, null=True),
        ),
    ]
