from django.db import models
from apps.core.models import AbstractBaseModel
from apps.policies.models import Policy

from apps.constants.choice_constants import (
    PAYMENT_METHODS,
    PAYMENT_PERIOD_CHOICES,
    CYCLE_CHOICE_TYPES,
    SCHEME_TYPE_CHOICES
)

from apps.sales.bulk_upload_methods import get_product_id_from_pricing_plan, get_policy_number_prefix


class Scheme(AbstractBaseModel):
    name = models.CharField(max_length=255)
    scheme_type = models.CharField(max_length=255, choices=SCHEME_TYPE_CHOICES)
    max_amount_of_members = models.IntegerField(default=1)
    description = models.TextField(null=True, blank=True)
    master_policy = models.BooleanField(default=False)
    is_group_scheme = models.BooleanField(default=False)
    config = models.JSONField(null=True)
    policy_number_starting_counter = models.PositiveIntegerField(default=1)


    def __str__(self):
        return self.name

    def get_policy_number(self, pricing_group) -> dict:
        product_id = get_product_id_from_pricing_plan(pricing_plan=pricing_group)

        prefix = get_policy_number_prefix(product_id)
        policies = Policy.objects.filter(policy_number__startswith=prefix).order_by('-policy_number_counter')
        
        policy_number_counter = self.policy_number_starting_counter

        if policies.count() > 0:
            policy_number_counter = policies.first().policy_number_counter + 1

        policy_number = f"{prefix}{policy_number_counter}"

        return {
            "policy_number": policy_number,
            "policy_number_counter": policy_number_counter
        }


class SchemeGroup(AbstractBaseModel):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    policy = models.OneToOneField(Policy, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    payment_method = models.CharField(max_length=255, choices=PAYMENT_METHODS)
    period_type = models.CharField(max_length=255, choices=PAYMENT_PERIOD_CHOICES)
    period_frequency = models.IntegerField(default=1)
    pricing_group = models.ForeignKey(
        "prices.PricingPlan", on_delete=models.CASCADE, null=True, blank=True
    )
    cycle_type = models.CharField(max_length=255, choices=CYCLE_CHOICE_TYPES)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

