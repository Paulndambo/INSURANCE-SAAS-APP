# Generated by Django 4.1.6 on 2023-06-28 23:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sales", "0008_temporarydependentimport_identification_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="temporarydependentimport",
            name="firstname",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="temporarydependentimport",
            name="lastname",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
