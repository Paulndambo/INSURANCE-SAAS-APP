from django.db import models

from apps.constants.choice_constants import (OBLIGATION_TYPES,
                                             PRICING_PLAN_KINDS,
                                             SCHEME_TYPE_CHOICES)
from apps.core.models import AbstractBaseModel


# Create your models here.
class PricingPlanCategory(AbstractBaseModel):
    name = models.CharField(max_length=255)
    kind = models.CharField(max_length=255, default="long_term", choices=PRICING_PLAN_KINDS)

    def __str__(self):
        return self.name


class PricingPlan(AbstractBaseModel):
    name = models.CharField(max_length=255)
    base_premium = models.DecimalField(max_digits=10, decimal_places=2)
    value_added_service = models.DecimalField(max_digits=10, decimal_places=2)
    total_premium = models.DecimalField(max_digits=10, decimal_places=2)
    group = models.CharField(max_length=255, choices=SCHEME_TYPE_CHOICES, null=True, blank=True)
    category = models.ForeignKey(PricingPlanCategory, on_delete=models.SET_NULL, null=True)
    policy_holder_cover_levels = models.JSONField(default=list)
    dependent_cover_levels = models.JSONField(default=list)
    extended_family_cover_levels = models.JSONField(default=list)

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
        return self.pricing_plan
    

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
    credit_reference = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.creditor_name


########## Medical Plans Specific Models ##########
class MedicalCover(AbstractBaseModel):
    pricing_plan = models.ForeignKey("prices.PricingPlan", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    inpatient_cover_amounts = models.JSONField(default=list)
    outpatient_cover_amounts = models.JSONField(default=list)

    def __str__(self):
        return self.name


class MedicalCoverPricing(AbstractBaseModel):
    medical_cover = models.ForeignKey(MedicalCover, on_delete=models.CASCADE)
    inpatient_cover = models.DecimalField(max_digits=30, decimal_places=2)
    outpatient_cover = models.DecimalField(max_digits=30, decimal_places=2)
    ph_age_group = models.CharField(max_length=255, null=True)
    ph_premium = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    spouse_age_group = models.CharField(max_length=255, null=True)
    spouse_premium = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    child_premium = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    outpatient_premium = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    inpatient_premium = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.medical_cover.name


### Motor Insurance  Specific Models ########