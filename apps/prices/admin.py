from django.contrib import admin

from apps.prices.models import (MedicalCover, MedicalCoverPricing, PricingPlan,
                                PricingPlanCategory)


# Register your models here.
@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ["name", "group", "category"]

@admin.register(PricingPlanCategory)
class PricingPlanCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "kind"]


@admin.register(MedicalCover)
class MedicalCover(admin.ModelAdmin):
    list_display = ["pricing_plan", "name", "inpatient_cover_amounts", "outpatient_cover_amounts"]

@admin.register(MedicalCoverPricing)
class MedicalCoverPricingAdmin(admin.ModelAdmin):
    list_display = ["medical_cover", "inpatient_cover", "outpatient_cover", "ph_age_group", "ph_premium", "spouse_age_group", "spouse_premium", "child_premium"]