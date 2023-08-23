from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from apps.core.models import AbstractBaseModel
from apps.policies.models import Policy
from apps.users.models import Membership
from apps.schemes.models import SchemeGroup

from apps.constants.choice_constants import (
    PAYMENT_PERIOD_CHOICES,
    PAYMENT_METHODS,
    PAYMENT_STATUS_CHOICES,
    ACCOUNT_TYPES,
)


# Create your models here.
class Bank(AbstractBaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    branch_code = models.TextField(blank=True)
    branch_name = models.TextField(blank=True)

    def __str__(self):
        return self.name


class BankStatement(AbstractBaseModel):
    policy_number = models.CharField(max_length=255, null=True)
    statement = models.JSONField(null=True)
    processed = models.BooleanField(default=False)
    


class PolicyPremium(AbstractBaseModel):
    RETRY_STAUSES = (
        ("error", "Error"),
        ("failed", "Failed"),
        ("pending", "Pending"),
        ("success", "Success"),
        ("unknown", "Unknown"),
    )

    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name="policypremiums")
    membership = models.ForeignKey("users.Membership", on_delete=models.CASCADE, null=True, related_name="membershipprems")
    bank_statement = models.ForeignKey("payments.BankStatement", on_delete=models.CASCADE, null=True)
    #payments = models.ManyToManyField(PolicyPayment, related_name="premiums")
    balance = models.FloatField()
    expected_payment = models.FloatField()
    expected_date = models.DateField()
    status = models.CharField(choices=PAYMENT_STATUS_CHOICES, default="future", max_length=32)
    detailed_balance = models.JSONField(default=list)
    payments_details = models.JSONField(default=list)
    reference = models.CharField(null=True, max_length=100)
    retry_on_date = models.DateField(null=True)
    retry_status = models.CharField(choices=RETRY_STAUSES, default="unknown", max_length=32)

    def __str__(self):
        return self.policy.policy_number



class PolicyPayment(AbstractBaseModel):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    membership = models.ForeignKey("users.Membership", on_delete=models.CASCADE, null=True)
    amount = models.FloatField(validators=[MinValueValidator(limit_value=0),], default=0)
    state = models.CharField(default="NEW", max_length=255)
    payment_method = models.CharField(choices=PAYMENT_METHODS, max_length=32)
    payment_date = models.DateField(null=True)
    premium = models.ForeignKey("payments.PolicyPremium", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.policy.policy_number


class DebitOrder(AbstractBaseModel):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    branch_code = models.CharField(max_length=64)
    account_number = models.CharField(max_length=64)
    account_type = models.CharField(choices=ACCOUNT_TYPES, max_length=32)
    accepted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    signature = models.ImageField(upload_to="signatures/", null=True)
    pdf = models.FileField(upload_to="debit_orders/", null=True)
    pdf_glacier_id = models.CharField(max_length=256, null=True)
    state = models.CharField(max_length=256, null=True)
    rejected_reason = models.CharField(max_length=256, null=True)
    agreement_reference_number = models.CharField(max_length=256, null=True, blank=True)
    request_identifier = models.TextField(null=True)
    attachment = models.FileField(upload_to="debit_order_attachments/", null=True)
    change_user_identifier = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE)
    branch_name = models.CharField(max_length=255, null=True)
    account_name = models.CharField(max_length=255, null=True)
    date = models.IntegerField(
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=31),
        ],
        null=True,
    )

    def __str__(self):
        return self.account_name


class FuturePremiumTracking(AbstractBaseModel):
    membership = models.ForeignKey("users.Membership", on_delete=models.SET_NULL, null=True)
    policy = models.ForeignKey("policies.Policy", on_delete=models.SET_NULL, null=True)
    expected_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    expected_date = models.DateField()
    future_expected_date = models.DateField(null=True)
    processed = models.BooleanField(default=False)


class CollectedPayment(AbstractBaseModel):
    pass