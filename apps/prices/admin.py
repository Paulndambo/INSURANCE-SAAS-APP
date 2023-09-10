from django.contrib import admin
from apps.prices.models import PricingPlan, PricingPlanCategory
# Register your models here.
@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ["name", "group", "category"]

@admin.register(PricingPlanCategory)
class PricingPlanCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "kind"]