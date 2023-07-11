# Generated by Django 4.1.6 on 2023-07-01 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("policies", "0004_remove_policy_broker_alter_policy_broker_information"),
        ("users", "0004_alter_user_role"),
        ("prices", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Obligation",
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
                ("creditor_name", models.CharField(max_length=255)),
                ("included", models.BooleanField(default=False)),
                (
                    "insurance_premium",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "original_balance",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "proposal_installment",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("inception_date", models.DateField(null=True)),
                (
                    "obligation_type",
                    models.CharField(
                        choices=[
                            ("obligation", "Obligation"),
                            ("3rd Party Insurance", "3rd Party Insurance"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "membership",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="users.membership",
                    ),
                ),
                (
                    "policy",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="policies.policy",
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="users.profile",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]