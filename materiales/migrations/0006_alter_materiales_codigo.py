# Generated by Django 5.0.3 on 2024-10-17 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0005_alter_materiales_gestion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materiales',
            name='codigo',
            field=models.CharField(max_length=255),
        ),
    ]