from django.contrib import admin
from .models import PolicyCancellation, Policy, PolicyStatusUpdates
# Register your models here.
admin.site.register(PolicyCancellation)
admin.site.register(PolicyStatusUpdates)

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ["id", "policy_number", "start_date", "status"]