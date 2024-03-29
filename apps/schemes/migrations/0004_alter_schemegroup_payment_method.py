# Generated by Django 4.1.7 on 2023-08-23 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemes', '0003_alter_schemegroup_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schemegroup',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Cash'), ('debit_order', 'Debit Order'), ('stop_order', 'Stop Order'), ('off_platform', 'Off Platform'), ('mpesa', 'Mpesa'), ('manual', 'Manual')], max_length=255),
        ),
    ]
