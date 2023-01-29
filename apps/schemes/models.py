from django.db import models
from apps.core.models import AbstractBaseModel
from apps.policies.models import Policy


SCHEME_TYPE_CHOICES = (
    ("retail", "Retail"),
    ("group", "Group"),
)

class Scheme(AbstractBaseModel):
    name = models.CharField(max_length=255)
    scheme_type = models.CharField(max_length=255)
    max_members_number = models.IntegerField(default=1)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


PAYMENT_METHODS = (
    ("cash", "Cash"),
    ("debit_order", "Debit Order"),
    ("stop_order", "Stop Order"),
    ("manual", "Manual"),
    ("off_platform", "Off Platform"),
    ("payu", "Payu"),
    ("paygate", "Pay Gate"),
)


PAYMENT_PERIOD_CHOICES = (
    ("weekly", "Weekly"),
    ("monthly", "Monthly"),
    ("quarterly", "Quarterly"),
    ("biannual", "Biannual"),
    ("yearly", "Yearly")
)

CYCLE_CHOICE_TYPES = (
    ("member", "Member"),
    ("group", "Group"),
)

class SchemeGroup(AbstractBaseModel):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    policy = models.OneToOneField(Policy, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    payment_method = models.CharField(max_length=255, choices=PAYMENT_METHODS)
    period_type = models.CharField(max_length=255, choices=PAYMENT_PERIOD_CHOICES)
    #pricing_group = models.ForeignKey(PricingPlan, on_delete=models.CASCADE)
    cycle_type = models.CharField(max_length=255, choices=CYCLE_CHOICE_TYPES)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

