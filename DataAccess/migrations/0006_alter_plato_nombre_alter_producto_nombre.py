# Generated by Django 4.1 on 2023-09-26 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("DataAccess", "0005_alter_restaurante_cantidadmesas_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plato", name="nombre", field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name="producto",
            name="nombre",
            field=models.CharField(max_length=200),
        ),
    ]