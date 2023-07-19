# Generated by Django 4.1.1 on 2023-07-18 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("entities", "0001_initial"),
        ("policies", "0004_remove_policy_broker_alter_policy_broker_information"),
    ]

    operations = [
        migrations.AddField(
            model_name="policy",
            name="sold_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="entities.salesagent",
            ),
        ),
    ]
