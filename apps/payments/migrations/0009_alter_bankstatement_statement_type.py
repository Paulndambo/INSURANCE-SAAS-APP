# Generated by Django 4.1.6 on 2023-06-17 18:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0008_alter_bankstatement_statement_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bankstatement",
            name="statement_type",
            field=models.CharField(
                choices=[("bank_statement", "Bank Statement"), ("receipt", "Receipt")],
                default="bank_statement",
                max_length=255,
            ),
        ),
    ]
