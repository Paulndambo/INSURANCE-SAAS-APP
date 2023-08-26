from django.contrib import admin
from apps.prices.models import PricingPlan, PricingPlanCategory
# Register your models here.
admin.site.register(PricingPlan)

@admin.register(PricingPlanCategory)
class PricingPlanCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "kind"]