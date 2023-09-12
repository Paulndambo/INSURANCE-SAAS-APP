from django.db import models

from apps.core.models import AbstractBaseModel


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
    ph_age_group = models.CharField(max_length=255)
    ph_premium = models.DecimalField(max_digits=10, decimal_places=2)
    spouse_premium = models.DecimalField(max_digits=10, decimal_places=2)
    child_premium = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.medical_cover.name