from django.db import models
from apps.core.models import AbstractBaseModel
from apps.policies.models import Policy

from apps.constants.choice_constants import (
    PAYMENT_METHODS,
    PAYMENT_PERIOD_CHOICES,
    CYCLE_CHOICE_TYPES,
)


class Scheme(AbstractBaseModel):
    name = models.CharField(max_length=255)
    scheme_type = models.CharField(max_length=255)
    max_members_number = models.IntegerField(default=1)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class SchemeGroup(AbstractBaseModel):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    policy = models.OneToOneField(Policy, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    payment_method = models.CharField(max_length=255, choices=PAYMENT_METHODS)
    period_type = models.CharField(max_length=255, choices=PAYMENT_PERIOD_CHOICES)
    period_frequency = models.IntegerField(default=1)
    pricing_group = models.ForeignKey("prices.PricingPlan", on_delete=models.CASCADE, null=True, blank=True)
    cycle_type = models.CharField(max_length=255, choices=CYCLE_CHOICE_TYPES)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
