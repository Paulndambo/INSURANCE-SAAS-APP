# Generated by Django 4.2.4 on 2023-09-01 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0008_remove_user_sub_role_alter_user_role"),
        ("dependents", "0008_remove_dependent_relative"),
    ]

    operations = [
        migrations.AddField(
            model_name="dependent",
            name="relative",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.policyholderrelative",
            ),
        ),
    ]