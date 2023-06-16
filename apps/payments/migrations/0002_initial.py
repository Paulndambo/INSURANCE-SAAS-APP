# Generated by Django 4.1.1 on 2023-06-15 12:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("payments", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0001_initial"),
        ("policies", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="policypremium",
            name="membership",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.membership",
            ),
        ),
        migrations.AddField(
            model_name="policypremium",
            name="payments",
            field=models.ManyToManyField(
                related_name="premiums", to="payments.policypayment"
            ),
        ),
        migrations.AddField(
            model_name="policypremium",
            name="policy",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="policies.policy"
            ),
        ),
        migrations.AddField(
            model_name="policypayment",
            name="bank_statement",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="payments.bankstatement",
            ),
        ),
        migrations.AddField(
            model_name="policypayment",
            name="membership",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.membership",
            ),
        ),
        migrations.AddField(
            model_name="policypayment",
            name="policy",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="policies.policy"
            ),
        ),
        migrations.AddField(
            model_name="debitorder",
            name="bank",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="payments.bank"
            ),
        ),
        migrations.AddField(
            model_name="debitorder",
            name="change_user_identifier",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="debitorder",
            name="policy",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="policies.policy"
            ),
        ),
    ]
