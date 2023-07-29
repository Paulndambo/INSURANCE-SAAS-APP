from django.contrib import admin
from apps.dependents.models import Dependent, Beneficiary
# Register your models here.
@admin.register(Dependent)
class DependentAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "id_number", "dependent_type", "relative", "cover_level", "add_on_premium"]

@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ["first_name", "id_number"]