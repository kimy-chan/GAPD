# Generated by Django 5.0.3 on 2024-09-22 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logs_sistema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('user', models.CharField(max_length=255)),
                ('accion', models.CharField(max_length=255)),
                ('detalle', models.TextField()),
                ('modelo', models.CharField(max_length=255)),
            ],
        ),
    ]
