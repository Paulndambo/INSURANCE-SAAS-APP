# Generated by Django 4.1.1 on 2023-06-15 16:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sales", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="temporarymemberdata",
            name="cover_level",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
