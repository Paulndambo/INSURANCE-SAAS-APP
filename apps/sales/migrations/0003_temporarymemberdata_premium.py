# Generated by Django 4.1.1 on 2023-06-16 05:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sales", "0002_temporarymemberdata_cover_level"),
    ]

    operations = [
        migrations.AddField(
            model_name="temporarymemberdata",
            name="premium",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]