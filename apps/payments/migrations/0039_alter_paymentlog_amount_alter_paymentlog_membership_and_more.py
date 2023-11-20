# Generated by Django 4.2.4 on 2023-09-21 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0009_alter_user_role"),
        ("payments", "0038_paymentlog_id_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymentlog",
            name="amount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name="paymentlog",
            name="membership",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.membership",
            ),
        ),
        migrations.AlterField(
            model_name="paymentlog",
            name="payment_date",
            field=models.DateField(null=True),
        ),
    ]