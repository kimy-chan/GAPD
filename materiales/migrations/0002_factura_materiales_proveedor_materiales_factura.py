# Generated by Django 5.0.3 on 2024-09-28 01:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0001_initial'),
        ('proveedor', '0003_remove_proveedor_prue'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nuemro_factural', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='materiales',
            name='proveedor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='proveedor.proveedor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='materiales',
            name='factura',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='materiales.factura'),
            preserve_default=False,
        ),
    ]
