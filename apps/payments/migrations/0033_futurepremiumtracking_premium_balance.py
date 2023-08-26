# Generated by Django 4.2.4 on 2023-08-25 04:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0032_alter_policypremium_reference"),
    ]

    operations = [
        migrations.AddField(
            model_name="futurepremiumtracking",
            name="premium_balance",
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]