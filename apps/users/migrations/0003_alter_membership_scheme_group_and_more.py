# Generated by Django 4.1.6 on 2023-06-17 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("schemes", "0001_initial"),
        ("users", "0002_alter_membershipconfiguration_membership"),
    ]

    operations = [
        migrations.AlterField(
            model_name="membership",
            name="scheme_group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="schemegroupmembers",
                to="schemes.schemegroup",
            ),
        ),
        migrations.AlterField(
            model_name="policyholder",
            name="individual_user",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="policyholders",
                to="users.individualuser",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="profiles",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]