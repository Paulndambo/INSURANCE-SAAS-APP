from django.contrib import admin
from .models import PolicyCancellation, Policy
# Register your models here.
admin.site.register(PolicyCancellation)

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ["id", "policy_number", "start_date", "status"]