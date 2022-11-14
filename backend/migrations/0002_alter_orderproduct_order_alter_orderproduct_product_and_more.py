# Generated by Django 4.1.2 on 2022-11-12 14:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderproduct",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="OrderProduct",
                to="backend.order",
                verbose_name="Заказ",
            ),
        ),
        migrations.AlterField(
            model_name="orderproduct",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="OrderProduct",
                to="backend.product",
                verbose_name="Товар",
            ),
        ),
        migrations.AlterField(
            model_name="orderproduct",
            name="shop",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="OrderProduct",
                to="backend.shop",
                verbose_name="Магазин",
            ),
        ),
        migrations.AlterField(
            model_name="orderproduct",
            name="shop_products",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shopproduct",
                to="backend.shopproducts",
                verbose_name="Наличие в магазине",
            ),
        ),
        migrations.AlterField(
            model_name="orderproduct",
            name="user",
            field=models.ForeignKey(
                auto_created=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="category",
                to="backend.category",
                verbose_name="Категория",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="user",
            field=models.ForeignKey(
                auto_created=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="shop",
            name="user",
            field=models.ForeignKey(
                auto_created=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="shopproducts",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product",
                to="backend.product",
                verbose_name="Товар",
            ),
        ),
        migrations.AlterField(
            model_name="shopproducts",
            name="shop",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shop",
                to="backend.shop",
                verbose_name="Магазин",
            ),
        ),
        migrations.AlterField(
            model_name="shopproducts",
            name="user",
            field=models.ForeignKey(
                auto_created=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
    ]
