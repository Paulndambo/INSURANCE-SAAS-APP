# Generated by Django 4.1.6 on 2023-07-03 05:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_user_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="membership",
            name="membership_premium",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]