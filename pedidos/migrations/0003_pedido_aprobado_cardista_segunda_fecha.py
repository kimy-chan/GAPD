# Generated by Django 5.0.3 on 2024-11-23 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='aprobado_cardista_segunda_fecha',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]