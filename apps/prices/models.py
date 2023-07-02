from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from apps.core.models import AbstractBaseModel
from apps.constants.choice_constants import SCHEME_TYPE_CHOICES, OBLIGATION_TYPES

# Create your models here.


class PricingPlan(AbstractBaseModel):
    name = models.CharField(max_length=255)
    base_premium = models.DecimalField(max_digits=10, decimal_places=2)
    value_added_service = models.DecimalField(max_digits=10, decimal_places=2)
    total_premium = models.DecimalField(max_digits=10, decimal_places=2)
    group = models.CharField(max_length=255, choices=SCHEME_TYPE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name


class PricingPlanCoverMapping(AbstractBaseModel):
    pricing_plan = models.ForeignKey(PricingPlan, on_delete=models.CASCADE)
    relationship = models.ForeignKey("users.PolicyHolderRelative", on_delete=models.PROTECT)
    cover_level = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    min_age = models.IntegerField(default=0)
    max_age = models.IntegerField(default=0)
    add_on_premium = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.pricing_plan.name


class PricingPlanExtendedPremiumMapping(AbstractBaseModel):
    pricing_plan = models.CharField(max_length=255)
    min_age = models.IntegerField(default=0)
    max_age = models.IntegerField(default=0)
    cover_level = models.DecimalField(max_digits=10, decimal_places=2)
    extended_premium = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.pricing_class


class PricingPlanDependentCoverPremiumMapping(AbstractBaseModel):
    pricing_type = models.CharField(max_length=255)
    dependent_category = models.CharField(max_length=255)
    dependent_type = models.CharField(max_length=255)
    min_age = models.IntegerField(default=0)
    max_age = models.IntegerField(default=0)
    cover_level = models.DecimalField(max_digits=10, decimal_places=2)
    premium = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.pricing_type


class PricingPlanSchemeMapping(AbstractBaseModel):
    name = models.CharField(max_length=255)
    scheme_type = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Obligation(AbstractBaseModel):
    profile = models.ForeignKey("users.Profile", on_delete=models.SET_NULL, null=True)
    membership = models.ForeignKey("users.Membership", on_delete=models.SET_NULL, null=True)
    policy = models.ForeignKey("policies.Policy", on_delete=models.SET_NULL, null=True)
    creditor_name = models.CharField(max_length=255)
    is_included = models.BooleanField(default=False)
    insurance_premium = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    original_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    proposal_installment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    inception_date = models.DateField(null=True)
    obligation_type = models.CharField(max_length=255, choices=OBLIGATION_TYPES)