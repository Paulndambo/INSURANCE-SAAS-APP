# Generated by Django 4.1.1 on 2023-07-25 14:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_membership_membership_premium"),
    ]

    operations = [
        migrations.RenameField(
            model_name="policyholder",
            old_name="address1",
            new_name="physical_address",
        ),
        migrations.RenameField(
            model_name="policyholder",
            old_name="identification_number",
            new_name="postal_address",
        ),
        migrations.RenameField(
            model_name="policyholder",
            old_name="phone1",
            new_name="work_phone",
        ),
        migrations.RenameField(
            model_name="profile",
            old_name="address",
            new_name="phone_number",
        ),
        migrations.RenameField(
            model_name="profile",
            old_name="address1",
            new_name="physical_address",
        ),
        migrations.RenameField(
            model_name="profile",
            old_name="identification_number",
            new_name="postal_address",
        ),
        migrations.RenameField(
            model_name="profile",
            old_name="phone",
            new_name="work_phone",
        ),
        migrations.RemoveField(
            model_name="policyholder",
            name="passport_number",
        ),
        migrations.RemoveField(
            model_name="policyholder",
            name="phone",
        ),
        migrations.RemoveField(
            model_name="policyholder",
            name="registration_number",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="passport_number",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="phone1",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="registration_number",
        ),
        migrations.AlterField(
            model_name="policyholderrelative",
            name="use_type",
            field=models.CharField(
                choices=[
                    ("main_member", "Main Member"),
                    ("dependent", "Dependent"),
                    ("beneficiary", "Beneficiary"),
                    ("parents", "Parents"),
                    ("stillborn", "Stillborn"),
                    ("extended", "Extended"),
                ],
                default="dependent",
                max_length=128,
            ),
        ),
    ]
