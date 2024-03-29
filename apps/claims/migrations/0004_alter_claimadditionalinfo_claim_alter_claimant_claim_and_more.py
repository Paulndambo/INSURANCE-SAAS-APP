# Generated by Django 4.1.1 on 2023-07-18 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("claims", "0003_claimgenericfieldlist_claim_dependent_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="claimadditionalinfo",
            name="claim",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="claimadditionalinfo",
                to="claims.claim",
            ),
        ),
        migrations.AlterField(
            model_name="claimant",
            name="claim",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="claimants",
                to="claims.claim",
            ),
        ),
        migrations.AlterField(
            model_name="claimdocument",
            name="claim",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="claimdocuments",
                to="claims.claim",
            ),
        ),
        migrations.AlterField(
            model_name="claimstatusupdates",
            name="claim",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="claimstatuses",
                to="claims.claim",
            ),
        ),
    ]
