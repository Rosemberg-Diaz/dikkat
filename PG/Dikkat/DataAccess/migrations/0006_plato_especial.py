# Generated by Django 4.1 on 2023-03-21 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("DataAccess", "0005_factura_productosfactura"),
    ]

    operations = [
        migrations.AddField(
            model_name="plato",
            name="especial",
            field=models.BooleanField(default=True),
        ),
    ]