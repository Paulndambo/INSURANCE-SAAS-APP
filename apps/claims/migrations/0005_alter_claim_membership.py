# Generated by Django 4.2.4 on 2023-09-26 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0010_alter_membership_user_alter_policyholder_gender_and_more"),
        (
            "claims",
            "0004_alter_claimadditionalinfo_claim_alter_claimant_claim_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="claim",
            name="membership",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="membershipsclaims",
                to="users.membership",
            ),
        ),
    ]
