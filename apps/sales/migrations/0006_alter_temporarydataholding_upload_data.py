# Generated by Django 4.1.1 on 2023-06-26 08:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "sales",
            "0005_remove_temporarycancelledmemberdata_main_member_identification_number_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="temporarydataholding",
            name="upload_data",
            field=models.JSONField(null=True),
        ),
    ]