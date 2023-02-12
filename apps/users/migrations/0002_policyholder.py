# Generated by Django 4.1.1 on 2023-01-29 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PolicyHolder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("id_number", models.CharField(max_length=255)),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "Male"), ("female", "Female")], max_length=255
                    ),
                ),
                ("marital_status", models.CharField(max_length=255)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("postal_address", models.CharField(max_length=255, null=True)),
                ("physical_address", models.CharField(max_length=255, null=True)),
                ("phone_number", models.CharField(max_length=255)),
                ("town", models.CharField(max_length=255, null=True)),
                ("country", models.CharField(max_length=255, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
