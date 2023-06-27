# Generated by Django 4.1.1 on 2023-06-26 08:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_membership_scheme_group_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("None", "Without role"),
                    ("admin", "C2S Admin"),
                    ("insurer", "Insurer"),
                    ("corporate", "Corporate"),
                    ("merchant", "Merchant"),
                    ("individual", "Individual"),
                    ("report_user", "Report User"),
                    ("technician_user", "Technician User"),
                    ("foh_user", "FOH User"),
                    ("customer_support_user", "Customer Support User"),
                    ("funeral_validator", "Funeral Validator"),
                    ("brokerage_admin", "Brokerage Admin"),
                    ("broker", "Broker"),
                    ("sales_agent", "Sales Agent"),
                    ("claim_validator", "Claim Validator"),
                    ("retail_agent", "Retail Agent"),
                ],
                default="individual",
                max_length=32,
            ),
        ),
    ]
