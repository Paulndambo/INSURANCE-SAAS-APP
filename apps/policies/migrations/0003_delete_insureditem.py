# Generated by Django 4.1.1 on 2023-02-16 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policies', '0002_policy_policy_holder'),
    ]

    operations = [
        migrations.DeleteModel(
            name='InsuredItem',
        ),
    ]
