# Generated by Django 4.1.6 on 2023-08-17 07:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dependents", "0003_beneficiary_relationship"),
    ]

    operations = [
        migrations.AddField(
            model_name="beneficiary",
            name="gender",
            field=models.CharField(
                choices=[("female", "Female"), ("male", "Male")],
                max_length=255,
                null=True,
            ),
        ),
    ]