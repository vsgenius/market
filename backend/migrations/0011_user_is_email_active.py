# Generated by Django 4.1.2 on 2022-11-13 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0010_alter_orderproduct_user_alter_user_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_email_active",
            field=models.BooleanField(default=False),
        ),
    ]