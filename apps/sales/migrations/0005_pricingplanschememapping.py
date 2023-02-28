# Generated by Django 4.1.1 on 2023-02-28 20:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sales", "0004_memberuploadoutcome"),
    ]

    operations = [
        migrations.CreateModel(
            name="PricingPlanSchemeMapping",
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
                ("name", models.CharField(max_length=255)),
                ("scheme_type", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
