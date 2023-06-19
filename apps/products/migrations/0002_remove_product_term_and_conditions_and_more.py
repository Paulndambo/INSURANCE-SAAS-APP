# Generated by Django 4.1.6 on 2023-06-17 18:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="term_and_conditions",
        ),
        migrations.AddField(
            model_name="product",
            name="disclosure_notice",
            field=models.FileField(null=True, upload_to="disclosure_notices/"),
        ),
        migrations.AddField(
            model_name="product",
            name="policy_wording",
            field=models.FileField(null=True, upload_to="policy_wordings/"),
        ),
    ]