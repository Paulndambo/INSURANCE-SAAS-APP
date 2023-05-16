from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from apps.core.models import AbstractBaseModel
from apps.constants.choice_constants import SCHEME_TYPE_CHOICES

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