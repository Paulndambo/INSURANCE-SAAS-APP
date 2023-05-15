# Generated by Django 4.1.1 on 2023-05-15 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("policies", "0013_remove_policy_payment_day_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cycle",
            name="status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("created", "Created"),
                    ("active", "Active"),
                    ("cancelled", "Cancelled"),
                    ("lapsed", "Lapsed"),
                    ("inactive", "Incative"),
                    ("ntu", "Not Taken Up"),
                    ("expired", "Expired"),
                    ("awaiting_payment", "Awaiting Payment"),
                ],
                default="draft",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="cyclestatusupdates",
            name="next_status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("created", "Created"),
                    ("active", "Active"),
                    ("cancelled", "Cancelled"),
                    ("lapsed", "Lapsed"),
                    ("inactive", "Incative"),
                    ("ntu", "Not Taken Up"),
                    ("expired", "Expired"),
                    ("awaiting_payment", "Awaiting Payment"),
                ],
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="cyclestatusupdates",
            name="previous_status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("created", "Created"),
                    ("active", "Active"),
                    ("cancelled", "Cancelled"),
                    ("lapsed", "Lapsed"),
                    ("inactive", "Incative"),
                    ("ntu", "Not Taken Up"),
                    ("expired", "Expired"),
                    ("awaiting_payment", "Awaiting Payment"),
                ],
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="policycancellation",
            name="status",
            field=models.CharField(
                choices=[
                    ("confirmed", "Confirmed"),
                    ("pending", "Pending"),
                    ("cancelled", "Cancelled"),
                ],
                default="pending",
                max_length=32,
            ),
        ),
        migrations.CreateModel(
            name="PolicyCancellationX",
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
                ("policy_previous_status", models.CharField(max_length=255)),
                ("policy_next_status", models.CharField(max_length=255)),
                (
                    "cancellation_status",
                    models.CharField(
                        choices=[
                            ("confirmed", "Confirmed"),
                            ("pending", "Pending"),
                            ("cancelled", "Cancelled"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "cancellation_origin",
                    models.CharField(
                        choices=[("customer", "Customer"), ("insurer", "Insurer")],
                        max_length=255,
                    ),
                ),
                (
                    "policy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="policies.policy",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
