# Generated by Django 5.0.3 on 2024-09-28 02:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0003_rename_nuemro_factural_factura_nuemro_factura_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='factura',
            old_name='nuemro_factura',
            new_name='codigo_factura',
        ),
    ]
