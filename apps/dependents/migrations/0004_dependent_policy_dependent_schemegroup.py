# Generated by Django 4.1.1 on 2023-04-03 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("policies", "0012_policy_product"),
        ("schemes", "0003_schemegroup_period_frequency"),
        ("dependents", "0003_dependent"),
    ]

    operations = [
        migrations.AddField(
            model_name="dependent",
            name="policy",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="policies.policy",
            ),
        ),
        migrations.AddField(
            model_name="dependent",
            name="schemegroup",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="schemes.schemegroup",
            ),
        ),
    ]