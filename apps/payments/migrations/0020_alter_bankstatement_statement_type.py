# Generated by Django 4.1.1 on 2023-03-16 08:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0019_alter_bankstatement_statement_type"),
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
