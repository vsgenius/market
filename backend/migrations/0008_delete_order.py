# Generated by Django 4.1.2 on 2022-11-13 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0007_orderproduct_price"),
    ]

    operations = [
        migrations.DeleteModel(name="Order",),
    ]