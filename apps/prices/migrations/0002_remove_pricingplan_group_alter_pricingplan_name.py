# Generated by Django 4.1.1 on 2023-02-16 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pricingplan',
            name='group',
        ),
        migrations.AlterField(
            model_name='pricingplan',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
