from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from apps.core.models import AbstractBaseModel

# Create your models here.


class PricingPlan(AbstractBaseModel):
    name = models.CharField(max_length=255)
    conditions = models.JSONField(default=dict, blank=True, null=True)
    matrix = models.JSONField(default=dict, blank=True)
    base_premium = models.FloatField(default=0,validators=[MinValueValidator(limit_value=0),],)
    value_added_service = models.FloatField(default=0,validators=[MinValueValidator(limit_value=0),],)
    total_premium = models.FloatField(default=0,validators=[MinValueValidator(limit_value=0),],)

    def __str__(self):
        return self.name
