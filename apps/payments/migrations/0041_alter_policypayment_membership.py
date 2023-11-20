# Generated by Django 4.2.4 on 2023-09-26 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0010_alter_membership_user_alter_policyholder_gender_and_more"),
        ("payments", "0040_paymentlog_balance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="policypayment",
            name="membership",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="membershippayments",
                to="users.membership",
            ),
        ),
    ]