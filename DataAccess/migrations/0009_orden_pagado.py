# Generated by Django 4.1 on 2023-09-26 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("DataAccess", "0008_factura_identificatororder"),
    ]

    operations = [
        migrations.AddField(
            model_name="orden", name="pagado", field=models.BooleanField(default=False),
        ),
    ]
