# Generated by Django 4.1.2 on 2022-11-13 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0006_remove_orderproduct_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderproduct",
            name="price",
            field=models.PositiveIntegerField(default=0, verbose_name="Цена"),
            preserve_default=False,
        ),
    ]
