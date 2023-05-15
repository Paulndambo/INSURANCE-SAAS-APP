# Generated by Django 4.1.1 on 2023-05-15 11:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0024_alter_bankstatement_statement_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bankstatement",
            name="statement_type",
            field=models.CharField(
                choices=[("receipt", "Receipt"), ("bank_statement", "Bank Statement")],
                default="bank_statement",
                max_length=255,
            ),
        ),
    ]
