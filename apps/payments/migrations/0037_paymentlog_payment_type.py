# Generated by Django 4.2.4 on 2023-09-21 05:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0036_policypayment_overpayment_policypayment_processed_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymentlog",
            name="payment_type",
            field=models.CharField(
                choices=[
                    ("bank", "Bank"),
                    ("card", "Card"),
                    ("mpesa", "Mpesa"),
                    ("manual", "Manual"),
                    ("bank_statement", "Bank Statement"),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]