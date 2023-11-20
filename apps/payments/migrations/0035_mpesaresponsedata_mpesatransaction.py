# Generated by Django 4.2.4 on 2023-09-18 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_remove_product_term_and_conditions_and_more"),
        ("payments", "0034_futurepremiumtracking_new_reference"),
    ]

    operations = [
        migrations.CreateModel(
            name="MpesaResponseData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("response_data", models.JSONField(default=dict)),
                ("response_description", models.CharField(max_length=1000)),
                ("response_code", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MpesaTransaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("MerchantRequestID", models.CharField(max_length=255)),
                ("CheckoutRequestID", models.CharField(max_length=255)),
                ("ResultCode", models.IntegerField(default=0)),
                ("ResultDesc", models.CharField(max_length=1000)),
                ("Amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("TransactionTimeStamp", models.CharField(max_length=255, null=True)),
                ("TransactionDate", models.DateTimeField()),
                ("PhoneNumber", models.CharField(max_length=255)),
                ("MpesaReceiptNumber", models.CharField(max_length=255)),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="products.product",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]