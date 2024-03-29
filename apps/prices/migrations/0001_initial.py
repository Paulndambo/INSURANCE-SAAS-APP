# Generated by Django 4.1.1 on 2023-06-15 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PricingPlan",
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
                ("base_premium", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "value_added_service",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("total_premium", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "group",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("retail", "Retail"),
                            ("group", "Group"),
                            ("credit", "Credit"),
                        ],
                        max_length=255,
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PricingPlanDependentCoverPremiumMapping",
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
                ("pricing_type", models.CharField(max_length=255)),
                ("dependent_category", models.CharField(max_length=255)),
                ("dependent_type", models.CharField(max_length=255)),
                ("min_age", models.IntegerField(default=0)),
                ("max_age", models.IntegerField(default=0)),
                ("cover_level", models.DecimalField(decimal_places=2, max_digits=10)),
                ("premium", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PricingPlanExtendedPremiumMapping",
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
                ("pricing_plan", models.CharField(max_length=255)),
                ("min_age", models.IntegerField(default=0)),
                ("max_age", models.IntegerField(default=0)),
                ("cover_level", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "extended_premium",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
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
        migrations.CreateModel(
            name="PricingPlanCoverMapping",
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
                (
                    "cover_level",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("min_age", models.IntegerField(default=0)),
                ("max_age", models.IntegerField(default=0)),
                (
                    "add_on_premium",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "pricing_plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="prices.pricingplan",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
