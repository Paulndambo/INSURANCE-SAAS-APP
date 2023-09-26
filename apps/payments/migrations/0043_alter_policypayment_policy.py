# Generated by Django 4.2.4 on 2023-09-26 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("policies", "0007_alter_policystatusupdates_policy"),
        ("payments", "0042_alter_paymentlog_membership"),
    ]

    operations = [
        migrations.AlterField(
            model_name="policypayment",
            name="policy",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="policypayments",
                to="policies.policy",
            ),
        ),
    ]
