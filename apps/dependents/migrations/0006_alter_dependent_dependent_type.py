# Generated by Django 4.2.4 on 2023-08-31 09:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dependents", "0005_dependent_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dependent",
            name="dependent_type",
            field=models.CharField(
                choices=[("dependent", "Dependent"), ("extended", "Extended")],
                max_length=200,
                null=True,
            ),
        ),
    ]
